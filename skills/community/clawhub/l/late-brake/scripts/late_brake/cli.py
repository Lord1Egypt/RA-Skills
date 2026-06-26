# -*- coding: utf-8 -*-
"""
Late Brake - CLI Entry Point

US-013: 赛道管理CLI框架 (track list/info/add)
US-010: 单次执行退出模式
US-011: 默认文本输出
US-012: JSON输出支持
"""

import json
import click
from typing import List, Optional
from wcwidth import wcswidth

from late_brake.io.track_store import (
    list_all_tracks,
    get_track_by_id,
    add_track_from_file,
)
from late_brake.models import Track


def padded(text: str, width: int, align: str = "left") -> str:
    """
    按实际显示宽度对齐文本，处理中文字符（每个中文占2宽度）
    :param text: 原始文本
    :param width: 目标显示宽度
    :param align: left/right
    :return: 对齐后文本
    """
    text_width = wcswidth(text)
    padding_needed = width - text_width
    if padding_needed <= 0:
        return text
    if align == "left":
        return text + " " * padding_needed
    else:
        return " " * padding_needed + text


def print_track_list_text(tracks: List[Track]) -> None:
    """默认文本格式输出赛道列表"""
    if not tracks:
        click.echo("没有已配置的赛道")
        return

    click.echo(f"\n已配置赛道 ({len(tracks)}):\n")
    for track in tracks:
        full_name = track.full_name if track.full_name else track.name
        if full_name != track.name:
            click.echo(f"  {track.id:6} - {full_name} ({track.name}) - {track.length_m}m, {track.turn_count} 弯道")
        else:
            click.echo(f"  {track.id:6} - {track.name} - {track.length_m}m, {track.turn_count} 弯道")
    click.echo()


def print_track_list_json(tracks: List[Track]) -> None:
    """JSON格式输出赛道列表"""
    data = [track.model_dump() for track in tracks]
    click.echo(json.dumps(data, indent=2, ensure_ascii=False))


def print_track_info_text(track: Track) -> None:
    """默认文本格式输出赛道详情"""
    click.echo()
    click.echo(f"ID:          {track.id}")
    click.echo(f"名称:        {track.name}")
    if track.full_name:
        click.echo(f"中文名:      {track.full_name}")
    if track.location:
        click.echo(f"位置:        {track.location}")
    click.echo(f"长度:        {track.length_m} 米")
    click.echo(f"弯道数:      {track.turn_count}")

    if track.sectors:
        click.echo(f"分段:        {len(track.sectors)} 个分段")
        for sector in track.sectors:
            turns = f"({len(sector.turns)} 弯道)" if sector.turns else ""
            click.echo(f"  - {sector.name}: {sector.start_distance_m}m - {sector.end_distance_m}m {turns}")

    if track.turns:
        click.echo(f"弯道:        {len(track.turns)} 个弯道")
        for turn in track.turns[:5]:
            click.echo(f"  - {turn.name}: {turn.type}, {turn.start_distance_m}m-{turn.end_distance_m}m")
        if len(track.turns) > 5:
            click.echo(f"  ... 还有 {len(track.turns) - 5} 个弯道")

    click.echo()


def print_track_info_json(track: Track) -> None:
    """JSON格式输出赛道详情"""
    click.echo(json.dumps(track.model_dump(), indent=2, ensure_ascii=False))


@click.group(invoke_without_command=False)
@click.version_option()
def cli():
    """Late Brake - 赛车圈速数据分析命令行工具

    用于对比分析不同圈速数据，帮助找出最佳走线和刹车时机。
    """
    pass


@click.group(name="track")
def track_group():
    """赛道管理命令

    管理内置和自定义赛道数据。
    """
    pass


@track_group.command(name="list")
@click.option("--json", "output_json", is_flag=True, default=False, help="输出JSON格式")
def track_list(output_json: bool):
    """列出所有已配置赛道"""
    try:
        tracks = list_all_tracks()
    except ValueError as e:
        if output_json:
            click.echo(json.dumps({"error": str(e)}, ensure_ascii=False))
        else:
            click.echo(f"错误: {e}")
        raise SystemExit(1)

    if output_json:
        print_track_list_json(tracks)
    else:
        print_track_list_text(tracks)


@track_group.command(name="info")
@click.argument("track_id")
@click.option("--json", "output_json", is_flag=True, default=False, help="输出JSON格式")
def track_info(track_id: str, output_json: bool):
    """显示指定赛道详细信息"""
    try:
        track = get_track_by_id(track_id)
    except ValueError as e:
        if output_json:
            click.echo(json.dumps({"error": str(e)}, ensure_ascii=False))
        else:
            click.echo(f"错误: {e}")
        raise SystemExit(1)

    if track is None:
        click.echo(f"错误: 赛道ID '{track_id}' 不存在")
        raise SystemExit(1)

    if output_json:
        print_track_info_json(track)
    else:
        print_track_info_text(track)


@track_group.command(name="add")
@click.argument("track_json_file")
def track_add(track_json_file: str):
    """从JSON文件添加或更新赛道"""
    success, msg, track = add_track_from_file(track_json_file)
    if not success:
        click.echo(f"错误: {msg}")
        raise SystemExit(1)

    click.echo()
    click.echo(f"✓ {msg}")
    click.echo()


# 注册子命令
cli.add_command(track_group)


@click.command(name="load")
@click.argument("data_files", nargs=-1, required=True)
@click.option("--track", "track_id", default=None, help="手动指定赛道ID")
@click.option("--json", "output_json", is_flag=True, default=False, help="输出JSON格式")
@click.option("--force-reload", "no_cache", is_flag=True, default=False, help="强制重新解析，忽略缓存 (别名: --no-cache)")
@click.option("--no-cache", "no_cache", is_flag=True, default=False, help="强制重新解析，忽略缓存")
def load_command(data_files, track_id, output_json, no_cache):
    """加载数据文件，自动匹配赛道并分割圈速，输出圈速列表

    解析结果缓存为 .{filename}.lb.json 以供后续对比使用
    """
    from late_brake.io.parsers import parse_file
    from late_brake.io.cache import save_cached_laps, load_cached_laps, remove_cached_laps
    from late_brake.core.matcher import match_track
    from late_brake.io.track_store import get_track_by_id
    from late_brake.core.splitter import split_laps
    from late_brake.models import Lap

    results = []
    any_failed = False

    for file_path in data_files:
        result = {
            "path": file_path,
            "success": False,
            "lap_count": 0,
            "laps": [],
            "error": None,
            "track_id": None,
            "track_name": None,
        }

        # 如果指定 --no-cache，先删除缓存
        if no_cache:
            remove_cached_laps(file_path)

        # 尝试加载缓存
        cached = None
        if not no_cache:
            cached = load_cached_laps(file_path)

        if cached is not None:
            # 缓存有效，直接使用
            laps = [Lap(**lap_data) for lap_data in cached["laps"]]
            cached_track_id = cached.get("track_id")
            track = get_track_by_id(cached_track_id) if cached_track_id else None
            if track is not None and laps:
                # 缓存可用
                result["success"] = True
                result["lap_count"] = len(laps)
                result["laps"] = [
                    {
                        "number": lap.lap_number,
                        "time": lap.total_time,
                        "is_complete": lap.is_complete,
                    }
                    for lap in laps
                ]
                result["track_id"] = track.id
                result["track_name"] = track.name
                results.append(result)
                continue

        # 解析文件
        points = parse_file(file_path)
        if points is None or len(points) == 0:
            result["error"] = "无法解析文件或没有有效数据点"
            results.append(result)
            any_failed = True
            continue

        # 获取赛道
        if track_id is not None:
            try:
                track = get_track_by_id(track_id)
            except ValueError as e:
                result["error"] = str(e)
                results.append(result)
                any_failed = True
                continue
            if track is None:
                result["error"] = f"指定的赛道ID '{track_id}' 不存在"
                results.append(result)
                any_failed = True
                continue
            match_msg = f"手动指定赛道: {track.id}"
        else:
            # 自动匹配
            try:
                track, match_msg = match_track(points)
            except ValueError as e:
                result["error"] = str(e)
                results.append(result)
                any_failed = True
                continue
            if track is None:
                result["error"] = match_msg
                results.append(result)
                any_failed = True
                continue

        # 分割圈速
        laps = split_laps(points, track, file_path)
        if not laps:
            result["error"] = "未能检测到任何圈速，请检查赛道是否正确"
            results.append(result)
            any_failed = True
            continue

        # 保存缓存
        save_cached_laps(file_path, laps, track.id)

        result["success"] = True
        result["lap_count"] = len(laps)
        result["laps"] = [
            {
                "number": lap.lap_number,
                "time": lap.total_time,
                "is_complete": lap.is_complete,
            }
            for lap in laps
        ]
        result["track_id"] = track.id
        result["track_name"] = track.name
        results.append(result)

    # 输出
    if output_json:
        click.echo(json.dumps({
            "files": results
        }, indent=2, ensure_ascii=False))
    else:
        click.echo()
        for res in results:
            click.echo(f"文件: {res['path']}")
            if not res["success"]:
                click.echo(f"  错误: {res['error']}")
            else:
                click.echo(f"  赛道: {res['track_id']} - {res['track_name']}")
                click.echo(f"  共 {res['lap_count']} 圈")
                for lap in res["laps"]:
                    mark = "" if lap["is_complete"] else " (不完整)"
                    minutes = int(lap["time"] // 60)
                    seconds = lap["time"] % 60
                    if minutes > 0:
                        time_str = f"{minutes}:{seconds:06.3f}"
                    else:
                        time_str = f"{seconds:.3f}"
                    click.echo(f"  Lap {lap['number']}: {time_str}{mark}")
            click.echo()

    if any_failed:
        raise SystemExit(1)


@click.command(name="compare")
@click.argument("file1_path")
@click.argument("lap1", type=int)
@click.argument("file2_path")
@click.argument("lap2", type=int)
@click.option("--track", "track_id", default=None, help="手动指定赛道ID")
@click.option("--json", "output_json", is_flag=True, default=False, help="输出JSON格式")
@click.option("--force-reload", "no_cache", is_flag=True, default=False, help="强制重新解析，忽略缓存 (别名: --no-cache)")
@click.option("--no-cache", "no_cache", is_flag=True, default=False, help="强制重新解析，忽略缓存")
def compare_command(file1_path, lap1, file2_path, lap2, track_id, output_json, no_cache):
    """对比两个文件中的任意两圈

    示例: late-brake compare file1.nmea 2 file2.vbo 4
    支持不同格式文件混对比，自动使用缓存
    """
    from late_brake.io.parsers import parse_file
    from late_brake.io.cache import load_cached_laps, remove_cached_laps, save_cached_laps
    from late_brake.core.matcher import match_track
    from late_brake.io.track_store import get_track_by_id
    from late_brake.core.splitter import split_laps
    from late_brake.core.comparator import compare_laps
    from late_brake.models import Lap

    def get_laps(file_path: str, track: Track) -> List[Lap]:
        """从缓存或重新解析获取圈速"""
        # 如果 --no-cache，先删除缓存
        if no_cache:
            remove_cached_laps(file_path)

        cached = load_cached_laps(file_path)
        if cached is not None and not no_cache:
            # 缓存存在且不强制重新加载，直接反序列化
            return [Lap(**lap_data) for lap_data in cached["laps"]]

        # 缓存不存在或强制重新加载，重新解析
        points = parse_file(file_path)
        if points is None or len(points) == 0:
            return []

        laps = split_laps(points, track, file_path)
        # 保存新缓存
        if track is not None:
            save_cached_laps(file_path, laps, track.id)

        return laps

    # 获取赛道
    # 如果没指定，尝试从第一个文件缓存获取，或自动匹配
    track = None
    if track_id is not None:
        try:
            track = get_track_by_id(track_id)
        except ValueError as e:
            if output_json:
                click.echo(json.dumps({"error": str(e)}, ensure_ascii=False))
            else:
                click.echo(f"错误: {e}")
            raise SystemExit(1)
        if track is None:
            click.echo(f"错误: 指定的赛道ID '{track_id}' 不存在")
            raise SystemExit(1)
    else:
        # 尝试从第一个文件缓存读取
        cached1 = load_cached_laps(file1_path)
        if cached1 is not None and cached1.get("track_id"):
            try:
                track = get_track_by_id(cached1["track_id"])
            except ValueError as e:
                if output_json:
                    click.echo(json.dumps({"error": str(e)}, ensure_ascii=False))
                else:
                    click.echo(f"错误: {e}")
                raise SystemExit(1)

        if track is None:
            # 缓存没有或匹配失败，自动匹配
            points1 = parse_file(file1_path)
            if points1 is None or len(points1) == 0:
                click.echo(f"错误: 无法解析 {file1_path} 进行赛道匹配")
                raise SystemExit(1)
            try:
                track, msg = match_track(points1)
            except ValueError as e:
                if output_json:
                    click.echo(json.dumps({"error": str(e)}, ensure_ascii=False))
                else:
                    click.echo(f"错误: {e}")
                raise SystemExit(1)
            if track is None:
                click.echo(f"错误: {msg}")
                raise SystemExit(1)

    # 获取两个文件的圈速
    laps1 = get_laps(file1_path, track)
    if not laps1:
        click.echo(f"错误: {file1_path} 中未能检测到任何圈")
        raise SystemExit(1)

    laps2 = get_laps(file2_path, track)
    if not laps2:
        click.echo(f"错误: {file2_path} 中未能检测到任何圈")
        raise SystemExit(1)

    # 找到指定圈号（用户输入1-based）
    if lap1 < 1 or lap1 > len(laps1):
        click.echo(f"错误: {file1_path} 中只有 {len(laps1)} 圈，不存在第 {lap1} 圈")
        raise SystemExit(1)
    lap_obj1 = laps1[lap1 - 1]

    if lap2 < 1 or lap2 > len(laps2):
        click.echo(f"错误: {file2_path} 中只有 {len(laps2)} 圈，不存在第 {lap2} 圈")
        raise SystemExit(1)
    lap_obj2 = laps2[lap2 - 1]

    # US-032: 检查两个 lap 是否都是完整圈
    incomplete = []
    if not lap_obj1.is_complete:
        incomplete.append(f"圈 {lap1} (来自 {file1_path})")
    if not lap_obj2.is_complete:
        incomplete.append(f"圈 {lap2} (来自 {file2_path})")
    if incomplete:
        msg = "无法对比不完整圈: " + "、".join(incomplete) + "\n只能对比两个完整圈，请选择其他圈重试"
        if output_json:
            click.echo(json.dumps({"error": msg}, ensure_ascii=False))
        else:
            click.echo(f"错误: {msg}")
        raise SystemExit(1)

    # 对比
    result = compare_laps(lap_obj1, lap_obj2, track)
    result["file1_path"] = file1_path
    result["file2_path"] = file2_path
    result["lap1_number"] = lap1
    result["lap2_number"] = lap2

    # 输出
    if output_json:
        click.echo(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        click.echo()
        click.echo(f"对比: {file1_path} 圈{lap1} vs {file2_path} 圈{lap2}")
        click.echo(f"赛道: {track.id} - {track.name}")
        click.echo()

        t1 = result["lap1"]["total_time"]
        t2 = result["lap2"]["total_time"]
        diff = result["total_time_diff"]

        m1 = int(t1 // 60)
        s1 = t1 % 60
        m2 = int(t2 // 60)
        s2 = t2 % 60

        if m1 > 0:
            lap1_str = f"{m1}:{s1:06.3f}"
        else:
            lap1_str = f"{s1:.3f}"
        if m2 > 0:
            lap2_str = f"{m2}:{s2:06.3f}"
        else:
            lap2_str = f"{s2:.3f}"

        click.echo(f"  圈1: {lap1_str}")
        click.echo(f"  圈2: {lap2_str}")
        click.echo()

        if diff < 0:
            click.echo(f"✓ 圈2更快，快 {abs(diff):.3f} 秒")
        elif diff > 0:
            click.echo(f"✓ 圈1更快，快 {diff:.3f} 秒")
        else:
            click.echo("圈速相同")

        click.echo()

        if result["sector_diff"]:
            click.echo("分段对比:")
            click.echo()
            # 使用padded对齐，处理中文字符宽度
            header = (
                "  " +
                padded("分段", 15, "left") +
                padded("时间(圈1)", 10, "right") +
                padded("时间(圈2)", 10, "right") +
                padded("时差", 8, "right") +
                padded("速度(圈1)", 10, "right") +
                padded("速度(圈2)", 10, "right") +
                padded("速差", 8, "right")
            )
            click.echo(header)
            click.echo("  " + "-" * 78)
            for sd in result["sector_diff"]:
                t1 = sd["time1"]
                t2 = sd["time2"]
                td = sd["time_diff"]
                av1 = sd["avg_speed1"]
                av2 = sd["avg_speed2"]
                svd = sd["avg_speed_diff"]
                name = sd["sector_name"][:12] + ("..." if len(sd["sector_name"]) > 12 else "")
                line = (
                    "  " +
                    padded(name, 15, "left") +
                    padded(f"{t1:.3f}", 10, "right") +
                    padded(f"{t2:.3f}", 10, "right") +
                    padded(f"{td:.3f}", 8, "right") +
                    padded(f"{av1:.2f}", 10, "right") +
                    padded(f"{av2:.2f}", 10, "right") +
                    padded(f"{svd:.2f}", 8, "right")
                )
                click.echo(line)
            click.echo()

        if result["turn_diff"]:
            click.echo("弯道对比:")
            click.echo()
            header = (
                "  " +
                padded("弯道", 6, "left") +
                padded("入速1", 8, "right") +
                padded("入速2", 8, "right") +
                padded("入差", 6, "right") +
                padded("心速1", 8, "right") +
                padded("心速2", 8, "right") +
                padded("心差", 6, "right") +
                padded("出速1", 8, "right") +
                padded("出速2", 8, "right") +
                padded("出差", 6, "right") +
                padded("均速1", 8, "right") +
                padded("均速2", 8, "right") +
                padded("均差", 6, "right") +
                padded("时差", 6, "right")
            )
            click.echo(header)
            click.echo("  " + "-" * 108)
            for td in result["turn_diff"]:
                line = (
                    "  " +
                    padded(td['turn_name'], 6, "left") +
                    padded(f"{td['speed_entry1']:.2f}", 8, "right") +
                    padded(f"{td['speed_entry2']:.2f}", 8, "right") +
                    padded(f"{td['speed_entry_diff']:.2f}", 6, "right") +
                    padded(f"{td['speed_apex1']:.2f}", 8, "right") +
                    padded(f"{td['speed_apex2']:.2f}", 8, "right") +
                    padded(f"{td['speed_apex_diff']:.2f}", 6, "right") +
                    padded(f"{td['speed_exit1']:.2f}", 8, "right") +
                    padded(f"{td['speed_exit2']:.2f}", 8, "right") +
                    padded(f"{td['speed_exit_diff']:.2f}", 6, "right") +
                    padded(f"{td['avg_speed1']:.2f}", 8, "right") +
                    padded(f"{td['avg_speed2']:.2f}", 8, "right") +
                    padded(f"{td['avg_speed_diff']:.2f}", 6, "right") +
                    padded(f"{td['time_diff']:.3f}", 6, "right")
                )
                click.echo(line)
            click.echo()

    # 对比总是成功
    pass


# 注册子命令
cli.add_command(load_command)
cli.add_command(compare_command)


def main():
    """CLI入口点，单次执行后退出（US-010）"""
    cli()


if __name__ == "__main__":
    main()
