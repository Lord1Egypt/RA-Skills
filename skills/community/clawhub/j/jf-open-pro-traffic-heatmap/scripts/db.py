"""SQLite 数据层 — 建表、检测记录写入、网格累积、查询"""

import sqlite3
from datetime import datetime
from typing import List, Dict, Any, Optional
from collections import defaultdict


def init_db(db_path: str) -> None:
    """创建数据库表（如不存在）"""
    conn = sqlite3.connect(db_path)
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS cameras (
            id          TEXT PRIMARY KEY,
            name        TEXT NOT NULL,
            password    TEXT NOT NULL,
            grid_cols   INTEGER DEFAULT 48,
            grid_rows   INTEGER DEFAULT 27,
            created_at  DATETIME DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS detections (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            camera_id   TEXT NOT NULL,
            timestamp   DATETIME NOT NULL,
            person_count INTEGER NOT NULL,
            image_path  TEXT
        );

        CREATE TABLE IF NOT EXISTS grid_heat (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            camera_id   TEXT NOT NULL,
            grid_row    INTEGER NOT NULL,
            grid_col    INTEGER NOT NULL,
            heat_count  INTEGER NOT NULL DEFAULT 0,
            window_start DATETIME NOT NULL,
            window_end  DATETIME NOT NULL
        );

        CREATE INDEX IF NOT EXISTS idx_grid_camera_time
            ON grid_heat(camera_id, window_start, window_end);
        CREATE INDEX IF NOT EXISTS idx_grid_cell
            ON grid_heat(camera_id, grid_row, grid_col);
        CREATE INDEX IF NOT EXISTS idx_detections_time
            ON detections(camera_id, timestamp);
    """)
    conn.commit()
    conn.close()


def insert_detections(db_path: str, camera_id: str, timestamp: datetime,
                      person_count: int, image_path: Optional[str] = None) -> None:
    """写入一帧的检测记录"""
    conn = sqlite3.connect(db_path)
    conn.execute(
        "INSERT INTO detections (camera_id, timestamp, person_count, image_path) "
        "VALUES (?, ?, ?, ?)",
        (camera_id, timestamp.isoformat(), person_count, image_path)
    )
    conn.commit()
    conn.close()


def accumulate_grid(db_path: str, camera_id: str, detections: List[Dict[str, int]],
                    window_start: datetime, window_end: datetime) -> None:
    """将检测到的坐标累积到网格热力表中"""
    if not detections:
        return

    cell_counts: Dict[tuple, int] = defaultdict(int)
    for d in detections:
        cell_counts[(d["row"], d["col"])] += 1

    conn = sqlite3.connect(db_path)
    ws = window_start.isoformat()
    we = window_end.isoformat()

    for (row, col), count in cell_counts.items():
        conn.execute(
            "INSERT INTO grid_heat (camera_id, grid_row, grid_col, heat_count, "
            "window_start, window_end) VALUES (?, ?, ?, ?, ?, ?)",
            (camera_id, row, col, count, ws, we)
        )

    conn.commit()
    conn.close()


def query_grid(db_path: str, camera_id: str, start: datetime,
               end: datetime) -> List[Dict[str, Any]]:
    """查询指定时间范围内的聚合网格数据"""
    conn = sqlite3.connect(db_path)
    rows = conn.execute(
        "SELECT grid_row, grid_col, SUM(heat_count) as heat_count "
        "FROM grid_heat "
        "WHERE camera_id = ? AND window_start >= ? AND window_start < ? "
        "GROUP BY grid_row, grid_col",
        (camera_id, start.isoformat(), end.isoformat())
    ).fetchall()
    conn.close()

    return [
        {"grid_row": r[0], "grid_col": r[1], "heat_count": r[2]}
        for r in rows
    ]


def query_time_series(db_path: str, camera_id: str, start: datetime,
                      end: datetime, interval_minutes: int = 10) -> List[Dict[str, Any]]:
    """按指定分钟间隔聚合检测数量，返回时间序列"""
    conn = sqlite3.connect(db_path)
    # 将 window_start 截断到 N 分钟窗口
    # strftime('%H')*60 + strftime('%M') 得到分钟数，除以间隔再乘回来
    rows = conn.execute(
        f"SELECT "
        f"  strftime('%H:%M', window_start, '-' || ((CAST(strftime('%M', window_start) AS INTEGER) % ?) || ' minutes')) as time_slot, "
        f"  SUM(heat_count) as count "
        f"FROM grid_heat "
        f"WHERE camera_id = ? AND window_start >= ? AND window_start < ? "
        f"GROUP BY time_slot ORDER BY time_slot",
        (interval_minutes, camera_id, start.isoformat(), end.isoformat())
    ).fetchall()
    conn.close()

    return [{"time": r[0], "count": r[1]} for r in rows]


def get_processed_images(db_path: str) -> set:
    """返回已处理过的图片路径集合，用于跳过重复处理"""
    conn = sqlite3.connect(db_path)
    rows = conn.execute(
        "SELECT DISTINCT image_path FROM detections WHERE image_path IS NOT NULL"
    ).fetchall()
    conn.close()
    return {r[0] for r in rows}


def query_history(db_path: str, camera_id: str, start: datetime,
                  end: datetime) -> List[Dict[str, Any]]:
    """查询检测历史记录（每条检测记录）"""
    conn = sqlite3.connect(db_path)
    rows = conn.execute(
        "SELECT timestamp, person_count, image_path "
        "FROM detections "
        "WHERE camera_id = ? AND timestamp >= ? AND timestamp < ? "
        "ORDER BY timestamp DESC",
        (camera_id, start.isoformat(), end.isoformat())
    ).fetchall()
    conn.close()
    return [
        {"timestamp": r[0], "person_count": r[1], "image_path": r[2]}
        for r in rows
    ]


def query_stats(db_path: str, camera_id: str, start: datetime,
                end: datetime) -> Dict[str, Any]:
    """查询汇总统计"""
    conn = sqlite3.connect(db_path)

    total = conn.execute(
        "SELECT COALESCE(SUM(heat_count), 0) FROM grid_heat "
        "WHERE camera_id = ? AND window_start >= ? AND window_start < ?",
        (camera_id, start.isoformat(), end.isoformat())
    ).fetchone()[0]

    peak_row = conn.execute(
        "SELECT CAST(strftime('%H', window_start) AS INTEGER) as hour, "
        "SUM(heat_count) as cnt FROM grid_heat "
        "WHERE camera_id = ? AND window_start >= ? AND window_start < ? "
        "GROUP BY hour ORDER BY cnt DESC LIMIT 1",
        (camera_id, start.isoformat(), end.isoformat())
    ).fetchone()
    peak_hour = peak_row[0] if peak_row else 0

    hot_row = conn.execute(
        "SELECT grid_row, grid_col, SUM(heat_count) as cnt FROM grid_heat "
        "WHERE camera_id = ? AND window_start >= ? AND window_start < ? "
        "GROUP BY grid_row, grid_col ORDER BY cnt DESC LIMIT 1",
        (camera_id, start.isoformat(), end.isoformat())
    ).fetchone()
    hottest = {"row": hot_row[0], "col": hot_row[1], "count": hot_row[2]} if hot_row else None

    rounds = conn.execute(
        "SELECT COUNT(DISTINCT window_start) FROM grid_heat "
        "WHERE camera_id = ? AND window_start >= ? AND window_start < ?",
        (camera_id, start.isoformat(), end.isoformat())
    ).fetchone()[0]

    conn.close()

    return {
        "total_detections": total,
        "peak_hour": peak_hour,
        "hottest_cell": hottest,
        "capture_rounds": rounds
    }
