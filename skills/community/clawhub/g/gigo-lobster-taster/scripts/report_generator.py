from __future__ import annotations
import html
import json
from datetime import datetime
from pathlib import Path
from string import Template

from .presentation import (
    build_focus_items,
    build_portrait_copy,
    build_public_metrics,
    build_skill_recommendations,
    derive_profile_tags,
    get_dimension_panels,
    get_tier_progress,
)


def _format_dimension_tags(config: dict, lang: str, keys: list[str]) -> str:
    labels: list[str] = []
    for key in keys:
        meta = config["dimensions"].get(key, {})
        label = meta.get(lang, key)
        emoji = meta.get("emoji", "")
        labels.append(f"{emoji} {label}".strip())
    return " / ".join(labels) if labels else ("—" if lang == "zh" else "—")


def _format_generated_at(timestamp: str, lang: str) -> str:
    try:
        parsed = datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
        if lang == "zh":
            return parsed.strftime("%Y.%m.%d %H:%M")
        return parsed.strftime("%Y-%m-%d %H:%M")
    except Exception:
        return timestamp.replace("T", " ").replace("Z", "")


def _tag_pills(tags: list[str]) -> str:
    return "".join(f'<span class="report-tag">{html.escape(tag)}</span>' for tag in tags)


def _dimension_cards(dimensions: dict[str, int], lang: str) -> str:
    cards = []
    for panel in get_dimension_panels(dimensions, lang):
        badge_class = (
            "tag-strong"
            if panel["score"] >= 85
            else "tag-medium"
            if panel["score"] >= 60
            else "tag-weak"
        )
        badges = "".join(f'<span class="sub-tag {badge_class}">{html.escape(str(badge))}</span>' for badge in panel["badges"])
        cards.append(
            f"""
            <article class="dim-card">
              <div class="dim-card-header">
                <div class="dim-icon" style="background:linear-gradient(135deg, color-mix(in srgb, {panel['color']} 92%, white 8%), color-mix(in srgb, {panel['color']} 72%, black 28%))">{html.escape(str(panel['icon']))}</div>
                <div class="dim-meta">
                  <div class="dim-name">{html.escape(str(panel['title']))}</div>
                  <div class="dim-desc">{html.escape(str(panel['description']))}</div>
                </div>
                <div class="dim-score-wrap">
                  <div class="dim-score" style="color:{panel['color']}">{panel['score']}</div>
                  <div class="dim-level {panel['level_key']}">{html.escape(str(panel['level']))}</div>
                </div>
              </div>
              <div class="dim-bar-track"><div class="dim-bar-fill" style="--tw:{panel['score']}%;background:linear-gradient(90deg,color-mix(in srgb,{panel['color']} 82%, transparent), {panel['color']})"></div></div>
              <div class="sub-tags">{badges}</div>
            </article>
            """
        )
    return "".join(cards)


def _focus_cards(dimensions: dict[str, int], lang: str, lock_tail: bool) -> str:
    items = build_focus_items(dimensions, lang)
    if not items:
        return (
            '<div class="empty-block">整体没有明显短板，这只龙虾已经很能打了。</div>'
            if lang == "zh"
            else '<div class="empty-block">There is no obvious weak point right now. This lobster is already very capable.</div>'
        )

    cards = []
    for index, item in enumerate(items):
        blur = False
        detail = "████████████████" if blur else html.escape(str(item["detail"]))
        cards.append(
            f"""
            <article class="imp-card {'blur' if blur else ''}">
              <div class="imp-rank">#{item['rank']}</div>
              <div class="imp-body">
                <div class="imp-title">{html.escape(str(item['icon']))} {html.escape(str(item['title']))}<span class="imp-score">（{item['score']}分）</span></div>
                <div class="imp-desc">{detail}</div>
              </div>
            </article>
            """
        )
    return "".join(cards)


def _skill_cards(dimensions: dict[str, int], lang: str) -> str:
    cards = []
    for item in build_skill_recommendations(dimensions, lang):
        badge_class = "sk-free" if item["badge_type"] == "free" else "sk-price"
        cards.append(
            f"""
            <a class="sk-card" href="https://clawhub.com" target="_blank" rel="noreferrer">
              <div class="sk-icon" style="background:linear-gradient(135deg, color-mix(in srgb, {item['color']} 92%, white 8%), color-mix(in srgb, {item['color']} 72%, black 28%))">{html.escape(str(item['icon']))}</div>
              <div class="sk-body">
                <div class="sk-name">{html.escape(str(item['name']))} <span class="{badge_class}">{html.escape(str(item['badge']))}</span></div>
                <div class="sk-desc">{html.escape(str(item['desc']))}</div>
              </div>
              <div class="sk-arrow">→</div>
            </a>
            """
        )
    return "".join(cards)


def _tier_steps(scores, lang: str) -> tuple[str, str]:
    progress = get_tier_progress(scores.total_score, scores.tier, lang)
    steps_html = "".join(
        f"""
        <div class="tier-step {'is-active' if step['active'] else ''} {'is-passed' if step['passed'] else ''}">
          <span class="tier-dot"></span>
          <strong>{html.escape(str(step['label']))}</strong>
        </div>
        """
        for step in progress["steps"]
    )

    if progress["gap"] > 0:
        copy = (
            f"距离 {progress['next_label']} 还差 {progress['gap']} 分"
            if lang == "zh"
            else f"{progress['gap']} points away from {progress['next_label']}"
        )
    else:
        copy = "已经来到最高段位" if lang == "zh" else "Already at the highest tier"
    return steps_html, copy


def _tier_compare(scores, lang: str) -> str:
    progress = get_tier_progress(scores.total_score, scores.tier, lang)
    steps = progress["steps"]
    current_index = next((index for index, step in enumerate(steps) if step["active"]), 0)
    prev_index = max(0, current_index - 1)
    next_index = min(len(steps) - 1, current_index + 1)
    previous = steps[prev_index]
    current = steps[current_index]
    upcoming = steps[next_index]
    current_label = "你的龙虾" if lang == "zh" else "Your lobster"
    current_score = scores.total_score
    prev_score = max(0, scores.total_score - max(4, progress["gap"] or 6))
    next_score = min(100, scores.total_score + max(3, progress["gap"] or 4))
    return f"""
      <div class="tier-cmp">
        <div class="tier-cmp-col">
          <span class="tier-cmp-emoji">◌</span>
          <div class="tier-cmp-name">{html.escape(str(previous['label']))}</div>
          <div class="tier-cmp-score">{prev_score}</div>
        </div>
        <div class="tier-cmp-col current">
          <span class="tier-cmp-emoji">●</span>
          <div class="tier-cmp-name">{html.escape(current_label)}</div>
          <div class="tier-cmp-score">{current_score}</div>
        </div>
        <div class="tier-cmp-col">
          <span class="tier-cmp-emoji">◌</span>
          <div class="tier-cmp-name">{html.escape(str(upcoming['label']))}</div>
          <div class="tier-cmp-score">{next_score}</div>
        </div>
      </div>
    """


def _overall_comment(scores, raw_results, config: dict, lang: str) -> tuple[str, str]:
    dimensions = scores.dimensions or {}
    if dimensions:
        ordered = sorted(dimensions.items(), key=lambda item: item[1], reverse=True)
        strongest_key, strongest_score = ordered[0]
        weakest_key, weakest_score = ordered[-1]
        strongest = config["dimensions"].get(strongest_key, {}).get(lang, strongest_key)
        weakest = config["dimensions"].get(weakest_key, {}).get(lang, weakest_key)
    else:
        strongest = weakest = "—"
        strongest_score = weakest_score = 0

    total = len(raw_results or [])
    success = sum(1 for result in raw_results or [] if result.status == "success")
    judged = sum(1 for result in raw_results or [] if result.judge_receipts)
    failed = [result.dish_name for result in raw_results or [] if result.status != "success"]

    if lang == "zh":
        title = "综合评语"
        base = (
            f"{scores.lobster_name} 这轮综合 {scores.total_score} 分，最稳定的是「{strongest}」"
            f"（{strongest_score} 分），最需要补的是「{weakest}」（{weakest_score} 分）。"
        )
        run = f"本轮完成 {success}/{total} 题"
        if judged:
            run += f"，其中 {judged} 题经过云端 judge 校验"
        run += "。"
        tail = (
            f"优先复盘「{failed[0]}」这类翻车题，再把低分维度拉到 60 分以上。"
            if failed
            else f"下一步优先把「{weakest}」从短板拉到稳定线，同时保住「{strongest}」的优势。"
        )
        return title, base + run + tail

    title = "Overall Note"
    base = (
        f"{scores.lobster_name} scored {scores.total_score}. The strongest dimension is {strongest} "
        f"({strongest_score}), while {weakest} needs the most work ({weakest_score})."
    )
    run = f" This run completed {success}/{total} tasks"
    if judged:
        run += f", with {judged} cloud-judged tasks"
    run += "."
    tail = (
        f" Start by reviewing failed tasks like {failed[0]}, then lift the weakest dimension above 60."
        if failed
        else f" Next, lift {weakest} without losing the current edge in {strongest}."
    )
    return title, base + run + tail


def _task_cards(raw_results, config: dict, lang: str) -> str:
    if not raw_results:
        return (
            '<div class="empty-block">当前没有可展示的任务记录。</div>'
            if lang == "zh"
            else '<div class="empty-block">There are no task records to show yet.</div>'
        )

    cards: list[str] = []
    for result in raw_results:
        primary = _format_dimension_tags(config, lang, result.primary_dimensions)
        secondary = _format_dimension_tags(config, lang, result.secondary_dimensions)
        status_label = (
            {"success": "通过", "timeout": "超时", "error": "翻车"}.get(result.status, result.status)
            if lang == "zh"
            else {"success": "Passed", "timeout": "Timed out", "error": "Failed"}.get(result.status, result.status)
        )
        if result.status == "error" and result.error:
            detail = f"运行错误：{result.error}" if lang == "zh" else f"Runtime error: {result.error}"
        elif result.status == "timeout":
            detail = "这一题超时，已按 0 分计入总评。" if lang == "zh" else "This task timed out and was counted as 0."
        else:
            detail = "这一题已计入综合评语和七维分数。" if lang == "zh" else "This task is reflected in the overall note and dimension scores."
        reasoning = (result.reasoning or "").strip()
        reasoning_block = ""
        if reasoning:
            summary = "查看评分依据" if lang == "zh" else "View judge note"
            meta = (
                "M2.7 只参与带 llm_judge 的题目评分；这里展示的是该题返回的简短 reasoning。"
                if lang == "zh"
                else "M2.7 is used only for tasks with llm_judge; this is the short reasoning returned for this task."
            )
            reasoning_block = f"""
              <details class="judge-note">
                <summary>
                  <span class="judge-note-title"><span class="judge-note-badge">M2.7</span>{html.escape(summary)}</span>
                </summary>
                <div class="judge-note-body">
                  <p>{html.escape(reasoning)}</p>
                  <div class="judge-note-meta">{html.escape(meta)}</div>
                </div>
              </details>
            """
        cards.append(
            f"""
            <article class="task-card">
              <div class="task-card-head">
                <div>
                  <h3>{html.escape(result.dish_name)}</h3>
                  <p>{html.escape(status_label)} · {result.total_score}/100</p>
                </div>
                <span>{result.elapsed_ms} ms</span>
              </div>
              <p class="task-copy">{html.escape(detail)}</p>
              {reasoning_block}
              <div class="task-meta-strip">
                <span>{'主维度' if lang == 'zh' else 'Primary'}: {html.escape(primary)}</span>
                <span>{'次维度' if lang == 'zh' else 'Secondary'}: {html.escape(secondary)}</span>
              </div>
            </article>
            """
        )
    return "".join(cards)


def generate_report(
    scores,
    raw_results,
    ref_code: str,
    config: dict,
    template_path: Path,
    upload_result: dict | None = None,
) -> Path:
    template = Template(template_path.read_text(encoding="utf-8"))
    threshold = int(config.get("unlock_threshold", 3))
    lang = scores.lang
    public_metrics = build_public_metrics(upload_result, ref_code, config)
    tier_steps_html, tier_copy = _tier_steps(scores, lang)

    total_entries = public_metrics["total_entries"]
    rank = public_metrics["rank"]
    surpassed = public_metrics["surpassed_percent"]

    if total_entries:
        total_entries_label = f"{total_entries:,}" if lang == "en" else f"{total_entries:,}"
    else:
        total_entries_label = "待同步" if lang == "zh" else "Pending"

    rank_label = f"#{rank}" if rank else ("未上榜" if lang == "zh" else "Unranked")
    surpassed_label = f"{surpassed:.1f}%" if isinstance(surpassed, float) else ("待同步" if lang == "zh" else "Pending")

    share_enabled = bool(public_metrics["share_enabled"])
    site_home_url = str(public_metrics.get("site_home_url") or config.get("site_home_url") or "https://eval.agent-gigo.com/")
    if share_enabled:
        unlock_message = (
            "把证书二维码或落地页发给朋友，每次成功打开都会推进一次完整诊断进度。"
            if lang == "zh"
            else "Share the certificate QR or landing page. Each successful open pushes the full diagnosis closer to unlock."
        )
        initial_remaining = threshold
        full_layer_display = "none"
        unlock_enabled = "true"
        local_mode_note = ""
    else:
        unlock_message = (
            "当前没有开启云端分享，这份本地报告已经直接展开完整诊断。"
            if lang == "zh"
            else "Cloud sharing is not enabled for this run, so the full diagnosis is already visible locally."
        )
        initial_remaining = 0
        full_layer_display = "block"
        unlock_enabled = "false"
        local_mode_note = (
            "这是本地私享版结果页。证书二维码会把朋友带到官网首页；如果想看到真正的线上结果页，需要先上传成绩。"
            if lang == "zh"
            else "This is the private local report. The certificate QR sends people to the homepage; a real online result page appears after the score is uploaded."
        )

    copy = {
        "stat_surpassed": "超越" if lang == "zh" else "Above",
        "stat_total": "已上榜" if lang == "zh" else "Ranked",
        "stat_rank": "排名" if lang == "zh" else "Rank",
        "portrait_kicker": "龙虾画像" if lang == "zh" else "Lobster portrait",
        "portrait_title": "画像概览" if lang == "zh" else "Profile",
        "radar_kicker": "能力雷达" if lang == "zh" else "Capability snapshot",
        "radar_title": "能力雷达" if lang == "zh" else "Radar",
        "dimension_kicker": "维度详情" if lang == "zh" else "Dimension breakdown",
        "dimension_title": "维度详情" if lang == "zh" else "Details",
        "tier_kicker": "段位进阶" if lang == "zh" else "Tier progress",
        "tier_title": "段位进阶" if lang == "zh" else "Tier progression",
        "focus_kicker": "待优化方向" if lang == "zh" else "What to tune next",
        "focus_title": "待优化方向" if lang == "zh" else "Next improvements",
        "share_kicker": "分享结果页" if lang == "zh" else "Share result page",
        "share_title": "分享结果页" if lang == "zh" else "Share result page",
        "full_kicker": "完整诊断" if lang == "zh" else "Full diagnosis",
        "full_title": "完整诊断" if lang == "zh" else "Full diagnosis",
        "full_hint": "分享结果页累计 3 次打开后，这里会展示 50 个任务卡片。每题只公开任务概览、耗时、维度分和简短得分依据；本地模式会直接展开。"
        if lang == "zh"
        else "After the shared result page records 3 opens, this section shows all 50 task cards with overview, time, dimensions, and a short public scoring basis; local-only reports show it immediately.",
        "landing_label": "扫码落地页" if lang == "zh" else "Scan landing page",
        "unlock_remaining": "还差 {remaining} 次打开，解锁完整诊断"
        if lang == "zh"
        else "{remaining} more opens to unlock the full diagnosis",
        "unlock_ready": "当前为本地模式，完整诊断已直接展开。"
        if lang == "zh"
        else "This run is local-only, so the full diagnosis is already visible.",
        "unlock_done": "完整诊断已解锁" if lang == "zh" else "Full diagnosis unlocked",
        "unlock_done_progress": "完整诊断已解锁，当前累计 {count} 次打开"
        if lang == "zh"
        else "Full diagnosis unlocked · {count} opens recorded",
        "radar_suffix": "七维全景" if lang == "zh" else "Seven-dimension view",
        "dimension_suffix": "子指标拆解" if lang == "zh" else "Sub-dimension breakdown",
        "rank_card_title": "你的龙虾在榜单里的位置" if lang == "zh" else "Your lobster's board position",
        "rank_card_button": "去网页查看排名" if lang == "zh" else "Open web ranking",
        "skill_kicker": "Skill 推荐" if lang == "zh" else "Skill picks",
        "skill_title": "针对性补足" if lang == "zh" else "Targeted upgrades",
        "share_button": "打开官网首页" if lang == "zh" else "Open homepage",
        "footer_time_label": "鉴定时间" if lang == "zh" else "Evaluated at",
        "share_hint": "证书二维码默认带朋友进入官网首页；真正的线上结果页会在上传成绩后生成。"
        if lang == "zh"
        else "The certificate QR opens the homepage first; the real online result page appears after the score is uploaded.",
        "footer_brand": "Powered by 🦞 龙虾试吃官"
        if lang == "zh"
        else "Powered by 🦞 Lobster Taster",
    }

    share_enabled = bool(public_metrics["share_enabled"])
    share_link_label = "线上结果页" if lang == "zh" else "Online result page"
    share_link_value = (
        str(public_metrics["share_url"])
        if share_enabled
        else ("本次未生成；上传成绩后才会有线上结果页" if lang == "zh" else "Not generated for this run. It appears after upload.")
    )
    landing_display_value = (
        str(public_metrics["landing_url"])
        if share_enabled
        else site_home_url
    )
    cta_primary_url = str(public_metrics["share_url"]) if share_enabled else site_home_url
    cta_rank_url = str(public_metrics["share_url"]) if share_enabled else site_home_url

    if share_enabled:
        copy["share_button"] = "打开分享结果页" if lang == "zh" else "Open result page"
        copy["rank_card_button"] = "去网页查看排名" if lang == "zh" else "Open web ranking"
        copy["share_hint"] = (
            "朋友扫证书会直接打开线上结果页，并自动记一次打开。达到阈值后，你本地报告里的完整诊断会自动解锁。"
            if lang == "zh"
            else "The certificate now opens the online result page directly and records one open automatically. Once the threshold is met, the full diagnosis unlocks inside your local report."
        )
    else:
        copy["rank_card_button"] = "打开官网首页" if lang == "zh" else "Open homepage"
        copy["share_hint"] = (
            "当前这轮没有上传成绩，所以不会生成个人线上结果页；证书二维码会打开官网首页。想分享给别人看你的专属结果，请先开启 upload / register。"
            if lang == "zh"
            else "This run did not upload a score, so no personal result page was created. The certificate QR opens the homepage. Use upload or register first if you want a shareable personal result."
        )

    task_total = len(raw_results or [])
    success_total = sum(1 for result in raw_results or [] if result.status == "success")
    overall_title, overall_comment = _overall_comment(scores, raw_results, config, lang)
    report_footer = (
        f"任务 {task_total} 题 · 成功 {success_total}/{task_total}"
        if lang == "zh"
        else f"{task_total} tasks · {success_total}/{task_total} passed"
    )

    rendered = template.safe_substitute(
        lang=lang,
        lobster_name=html.escape(scores.lobster_name),
        tier_name=html.escape(scores.tier_name),
        total_score=scores.total_score,
        portrait_copy=html.escape(build_portrait_copy(scores.dimensions, lang)),
        overall_title=html.escape(overall_title),
        overall_comment=html.escape(overall_comment),
        tag_pills=_tag_pills(derive_profile_tags(scores.dimensions, lang)),
        dimension_cards=_dimension_cards(scores.dimensions, lang),
        focus_cards=_focus_cards(scores.dimensions, lang, share_enabled),
        skill_cards=_skill_cards(scores.dimensions, lang),
        tier_steps=tier_steps_html,
        tier_progress_copy=html.escape(tier_copy),
        tier_compare=_tier_compare(scores, lang),
        task_cards=_task_cards(raw_results, config, lang),
        dimensions_json=json.dumps(scores.dimensions, ensure_ascii=False),
        ref_code=ref_code if share_enabled else "",
        api_base=config["api_base"].rstrip("/"),
        threshold=threshold,
        initial_remaining=initial_remaining,
        poll_initial_seconds=int(config.get("report_poll_initial_seconds", 10)),
        poll_slow_seconds=int(config.get("report_poll_slow_seconds", 60)),
        generated_at=html.escape(_format_generated_at(scores.timestamp, lang)),
        bundle_version=html.escape(str(config.get("task_bundle_version", "unknown"))),
        judge_model=html.escape(scores.judge_model),
        share_url=html.escape(str(public_metrics["share_url"])),
        landing_url=html.escape(landing_display_value),
        share_link_label=html.escape(share_link_label),
        share_link_value=html.escape(share_link_value),
        cta_primary_url=html.escape(cta_primary_url),
        cta_rank_url=html.escape(cta_rank_url),
        total_entries_label=html.escape(total_entries_label),
        rank_label=html.escape(rank_label),
        surpassed_label=html.escape(surpassed_label),
        unlock_message=html.escape(unlock_message),
        local_mode_note=html.escape(local_mode_note),
        unlock_enabled=unlock_enabled,
        full_layer_display=full_layer_display,
        partial_label="阶段性报告" if scores.partial and lang == "zh" else "Partial report" if scores.partial else "完整结果" if lang == "zh" else "Full result",
        radar_labels_json=json.dumps(
            {key: config["dimensions"][key].get(lang, key) for key in ["meat", "brain", "claw", "shell", "soul", "cost", "speed"]},
            ensure_ascii=False,
        ),
        stat_surpassed=copy["stat_surpassed"],
        stat_total=copy["stat_total"],
        stat_rank=copy["stat_rank"],
        portrait_kicker=copy["portrait_kicker"],
        portrait_title=copy["portrait_title"],
        radar_kicker=copy["radar_kicker"],
        radar_title=copy["radar_title"],
        dimension_kicker=copy["dimension_kicker"],
        dimension_title=copy["dimension_title"],
        tier_kicker=copy["tier_kicker"],
        tier_title=copy["tier_title"],
        focus_kicker=copy["focus_kicker"],
        focus_title=copy["focus_title"],
        share_kicker=copy["share_kicker"],
        share_title=copy["share_title"],
        full_kicker=copy["full_kicker"],
        full_title=copy["full_title"],
        full_hint=html.escape(copy["full_hint"]),
        landing_label=copy["landing_label"],
        unlock_remaining_template=copy["unlock_remaining"],
        unlock_ready_text=copy["unlock_ready"],
        unlock_done_text=copy["unlock_done"],
        unlock_done_progress_text=copy["unlock_done_progress"],
        radar_suffix=copy["radar_suffix"],
        dimension_suffix=copy["dimension_suffix"],
        rank_card_title=copy["rank_card_title"],
        rank_card_button=copy["rank_card_button"],
        skill_kicker=copy["skill_kicker"],
        skill_title=copy["skill_title"],
        share_button=copy["share_button"],
        footer_time_label=copy["footer_time_label"],
        share_hint=copy["share_hint"],
        footer_brand=copy["footer_brand"],
        task_summary=html.escape(report_footer),
    )
    output_path = Path(config["output_dir"]) / "lobster-report.html"
    output_path.write_text(rendered, encoding="utf-8")
    return output_path
