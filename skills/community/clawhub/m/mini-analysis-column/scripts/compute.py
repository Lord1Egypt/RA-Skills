#coding=utf-8
import pandas as pd
import traceback


def get_tb_info():
    return traceback.format_exc()


def main():
    msg  = "success"
    flag = 0
    dst  = {}

    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--file',   required=True)
    parser.add_argument('--rowkey', required=True)
    parser.add_argument('--debug', action='store_true', help='用于调试')
    args = parser.parse_args()

    try:
        data_df = pd.read_csv(args.file)
        if args.debug:
            print(data_df.shape)
            print(data_df.head(3))

        maxv  = data_df[args.rowkey].max()
        minv  = data_df[args.rowkey].min()
        meanv = data_df[args.rowkey].mean()
        dst["最大值"] = maxv
        dst["最小值"] = minv
        dst["平均值"] = meanv
        if args.debug:
            print(f"maxv =={maxv}")
            print(f"minv =={minv}")
            print(f"meanv=={meanv}")
    except Exception:
        msg = get_tb_info()
        flag = -1
        dst = None

    if flag == -1:
        print("程序调用失败")
        if args.debug:
            print(msg)
    else:
        print("程序调用成功")
        for key in dst:
            value = round(dst[key], 2)
            print(f"{key}: {value}")


if __name__ == "__main__":
    main()
