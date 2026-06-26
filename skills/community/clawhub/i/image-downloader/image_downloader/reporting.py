def build_run_report(
    keyword,
    requested_limit,
    collected_count,
    deduped_count,
    downloaded_count,
    skipped_count,
    output_dir,
    source_counts,
):
    lines = [
        f"关键词: {keyword}",
        f"目标下载数: {requested_limit}",
        f"候选总数: {collected_count}",
        f"去重后数量: {deduped_count}",
        f"实际成功下载: {downloaded_count}",
        f"跳过重复: {skipped_count}",
        "来源统计:",
    ]

    for source_name, count in source_counts.items():
        lines.append(f"- {source_name}: {count}")

    lines.append(f"保存目录: {output_dir}")
    return "\n".join(lines)
