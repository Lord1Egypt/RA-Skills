import json
import sys
import argparse
import pandas as pd
import numpy as np
from statsmodels.tsa.seasonal import STL
from datetime import datetime


def infer_period_from_timestamps(times: list):
    """
    Infer sampling frequency and seasonal period from timestamp list.
    Returns a dict with freq label, delta in seconds, and recommended period.
    """
    try:
        dt_list = pd.to_datetime(times)
        deltas = np.diff(dt_list).astype("timedelta64[s]").astype(int)
        delta_sec = int(np.median(deltas))

        if delta_sec <= 60:
            freq = "分钟"
            period = 60
        elif delta_sec <= 3600:
            freq = "小时"
            period = 24
        elif delta_sec <= 86400:
            freq = "日"
            period = 7
        elif delta_sec <= 7 * 86400:
            freq = "周"
            period = 4
        elif delta_sec <= 30 * 86400:
            freq = "月"
            period = 12
        else:
            freq = "未知"
            period = 7

        return {
            "freq": freq,
            "delta_seconds": delta_sec,
            "period": period,
            "msg": f"自动识别：{freq} 数据，周期 period={period}",
        }
    except Exception as e:
        return {
            "freq": "未知",
            "delta_seconds": 0,
            "period": 7,
            "msg": f"自动识别失败：{str(e)}",
        }


def detect_stl_3sigma_auto_period(times: list, values: list, sigma: int = 3):
    """
    Detect anomalies using STL decomposition + 3-sigma rule on residuals.
    Returns a structured result dict regardless of success or failure.
    """
    result = {
        "success": False,
        "column": None,
        "auto_infer": None,
        "period_used": None,
        "anomaly_count": 0,
        "threshold": {"upper": None, "lower": None},
        "anomalies": [],
        "error": None,
    }

    try:
        if len(times) != len(values):
            result["error"] = "时间与数值长度不一致"
            return result

        # Automatic period inference
        infer = infer_period_from_timestamps(times)
        result["auto_infer"] = infer
        period = infer["period"]

        # Guard: STL requires at least 2*period + 1 observations
        min_required = 2 * period + 1
        if len(values) < min_required:
            result["error"] = (
                f"数据量不足：需要至少 {min_required} 个点才能进行 STL 分解，"
                f"当前只有 {len(values)} 个点"
            )
            return result

        # Build time-series
        ts = pd.Series(values, index=pd.to_datetime(times))
        stl = STL(ts, period=period).fit()
        residual = stl.resid
        mean = residual.mean()
        std = residual.std()
        upper = mean + sigma * std
        lower = mean - sigma * std
        anomalies = ts[(residual > upper) | (residual < lower)]

        # Populate result
        result["success"] = True
        result["period_used"] = period
        result["anomaly_count"] = len(anomalies)
        result["threshold"] = {
            "upper": round(float(upper), 4),
            "lower": round(float(lower), 4),
        }

        for timestamp, value in anomalies.items():
            result["anomalies"].append(
                {
                    "timestamp": str(timestamp),
                    "value": float(value),
                }
            )

        # Human-readable console output (preserved for backward compatibility)
        print(f"auto_infer: {infer}")
        print(f"period_used: {period}")
        print(f"anomaly_count: {len(anomalies)}")
        print(f"threshold: upper: {round(float(upper), 4)}, lower: {round(float(lower), 4)}")
        if len(anomalies) > 0:
            print("===== anomaly points（timestamp → value）=====")
            for timestamp, value in anomalies.items():
                print(f"timestamp：{timestamp}\t value：{value}")
        else:
            print("No anomaly point being detected")

    except Exception as e:
        result["error"] = str(e)
        print(f"error: {str(e)}")

    return result


def parse_sensor_json(rawdata):
    """
    Parse JSON result into column-oriented dicts.
    """
    columns = rawdata["columns"]
    rows = rawdata["rows"]
    column_data = [list(col) for col in zip(*rows)]
    data_map = dict(zip(columns, column_data))

    return columns, data_map


def main():
    parser = argparse.ArgumentParser(
        description="KWDB Time-Series Anomaly Detection (STL + 3-sigma)"
    )
    parser.add_argument(
        "--input",
        nargs="?",
        help="Path to JSON file containing query result. Reads from stdin if omitted.",
    )
    parser.add_argument(
        "--output",
        "-o",
        dest="output_path",
        help="Optional path to write structured JSON result.",
    )
    parser.add_argument(
        "--sigma",
        type=int,
        default=3,
        help="Sigma multiplier for threshold (default: 3).",
    )
    args = parser.parse_args()

    # Load JSON
    try:
        if args.input:
            with open(args.input, "r", encoding="utf-8") as f:
                rawdata = json.load(f)
        else:
            rawdata = json.load(sys.stdin)
    except FileNotFoundError:
        print(f"错误：未找到文件 {args.input}")
        sys.exit(1)
    except json.JSONDecodeError:
        print("错误：输入不是有效的JSON格式")
        sys.exit(1)
    except Exception as e:
        print(f"读取输入失败: {e}")
        sys.exit(1)

    # Parse
    try:
        columns, column_data = parse_sensor_json(rawdata)
    except KeyError as e:
        print(f"错误：JSON格式不正确，缺少字段: {e}")
        sys.exit(1)

    print("文件解析成功！")
    timestamp_col = columns[0]
    all_results = []

    for col_name in columns[1:]:
        print(f"\n--- Detecting column: {col_name} ---")
        result = detect_stl_3sigma_auto_period(
            column_data[timestamp_col],
            column_data[col_name],
            sigma=args.sigma,
        )
        result["column"] = col_name
        all_results.append(result)

    # Optional structured output
    if args.output_path:
        try:
            with open(args.output_path, "w", encoding="utf-8") as f:
                json.dump(all_results, f, ensure_ascii=False, indent=2)
            print(f"\nStructured result written to: {args.output_path}")
        except Exception as e:
            print(f"\nFailed to write output file: {e}")
            sys.exit(1)


if __name__ == "__main__":
    main()