"""
normalize.py — 将 ClawHub + SkillHub 数据归一化为统一 schema

输入：
  data/snapshots/{date}.clawhub.json  — ClawHub 原始快照
  data/snapshots/{date}.skillhub.json — SkillHub 原始快照

输出：
  data/snapshots/{date}.merged.json — 合并去重后的统一 schema
    {
      "snapshot_date": "YYYY-MM-DD",
      "fetched_at": "ISO",
      "clawhub_count": N,
      "skillhub_count": N,
      "merged_count": N,
      "skills": [
        {
          "slug": "...",
          "name": "...",
          "description": "...",
          "description_zh": "...",
          "source": "clawhub|skillhub|both",
          "clawhub": { raw clawhub skill or null },
          "skillhub": { raw skillhub skill or null },
          "unified": {
            "slug": "...",
            "name": "...",
            "description": "...",
            "categories": [...],
            "tags": [...],
            "installs": {
              "clawhub": N or 0,
              "skillhub": N or 0,
              "total": N
            },
            "stars": {
              "clawhub": N or 0,
              "skillhub": N or 0,
              "total": N
            },
            "downloads": {
              "clawhub": N or 0,
              "skillhub": N or 0,
              "total": N
            },
            "versions_count": N,
            "created_at": "ISO",
            "updated_at": "ISO",
            "age_days": N,
            "days_since_update": N,
            "owner": "ownerName",
            "verified": bool,
            "has_changelog": bool,
            "latest_changelog": "..." or null,
            "ratings_count": N,
            "platforms_active": ["clawhub", "skillhub"] or ["clawhub"] or ["skillhub"]
          }
        }
      ]
    }
"""
from __future__ import annotations

import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path


def _slug_normalize(slug: str) -> str:
    """统一 slug 用于跨平台匹配：去 -cn/-zh 后缀，转小写。"""
    if not slug:
        return ""
    s = slug.lower().strip()
    # 去掉常见的中文/区域后缀
    s = re.sub(r"-(cn|zh|en|china|chinese)$", "", s)
    return s


def _safe_int(v, default=0) -> int:
    try:
        if v is None:
            return default
        return int(v)
    except (ValueError, TypeError):
        return default


def _safe_float(v, default=0.0) -> float:
    try:
        if v is None:
            return default
        return float(v)
    except (ValueError, TypeError):
        return default


def _to_iso(v) -> str | None:
    if not v:
        return None
    if isinstance(v, (int, float)):
        # 毫秒时间戳
        try:
            ts = v / 1000 if v > 1e12 else v
            return datetime.fromtimestamp(ts, tz=timezone.utc).isoformat()
        except (ValueError, OSError):
            return None
    if isinstance(v, str):
        return v
    return None


def _age_days(v) -> int | None:
    iso = _to_iso(v)
    if not iso:
        return None
    try:
        dt = datetime.fromisoformat(iso.replace("Z", "+00:00"))
        return max(0, (datetime.now(tz=timezone.utc) - dt).days)
    except (ValueError, TypeError):
        return None


def _flatten_tags_list(items) -> list[str]:
    """将 list 中的 dict 元素提取为字符串，统一返回 list[str]。"""
    result: list[str] = []
    if not items:
        return result
    if isinstance(items, dict):
        # tags 是 dict（如 ClawHub {"latest": "version_id"}），取 keys
        for k, v in items.items():
            if isinstance(v, str) and v:
                result.append(k)
            elif isinstance(v, dict):
                name = v.get("name") or v.get("slug") or v.get("key")
                if name:
                    result.append(str(name))
        return result
    if not isinstance(items, (list, tuple, set)):
        return result
    for t in items:
        if isinstance(t, str):
            if t:
                result.append(t)
        elif isinstance(t, dict):
            name = t.get("name") or t.get("slug") or t.get("key") or t.get("id")
            if name:
                result.append(str(name))
        elif isinstance(t, (list, tuple)):
            result.extend(_flatten_tags_list(t))
    return result


def _normalize_clawhub(raw: dict) -> dict:
    """归一化单个 ClawHub skill。ClawHub 数据是嵌套结构：raw.skill / raw.owner / raw.latestVersion。"""
    skill = raw.get("skill") or raw  # 兼容：如果传入的是已扁平化的 skill，直接用
    stats = skill.get("stats") or {}
    latest_version = raw.get("latestVersion") or {}
    owner_info = raw.get("owner") or {}
    badges = skill.get("badges") or {}

    installs = _safe_int(stats.get("installsCurrent") or stats.get("installs"))
    downloads = _safe_int(stats.get("downloads") or stats.get("installsAllTime"))
    stars = _safe_int(stats.get("stars") or stats.get("stargazers"))
    slug = skill.get("slug", "") or raw.get("slug", "")
    owner_handle = owner_info.get("handle") or owner_info.get("displayName") or raw.get("ownerHandle", "")

    return {
        "slug": slug,
        "name": skill.get("displayName", "") or raw.get("displayName", ""),
        "description": skill.get("summary", "") or raw.get("summary", "") or "",
        "categories": _flatten_tags_list(skill.get("categories") or []),
        "tags": _flatten_tags_list(skill.get("capabilityTags") or skill.get("topics") or []),
        "installs": installs,
        "downloads": downloads,
        "stars": stars,
        "ratings_count": _safe_int(stats.get("ratingsCount") or stats.get("comments")),
        "versions_count": _safe_int(stats.get("versions")),
        "created_at": _to_iso(skill.get("createdAt") or skill.get("_creationTime")),
        "updated_at": _to_iso(latest_version.get("createdAt") or skill.get("updatedAt")),
        "owner": owner_handle,
        "verified": bool(badges.get("verified")),
        "has_changelog": bool(latest_version.get("changelog")),
        "latest_changelog": latest_version.get("changelog"),
        "source_url": f"https://clawhub.ai/{owner_handle}/{slug}" if owner_handle and slug else f"https://clawhub.ai/skills/{slug}",
    }


def _normalize_skillhub(raw: dict) -> dict:
    """归一化单个 SkillHub skill。SkillHub 数据是扁平结构。"""
    slug = raw.get("slug", "")
    owner = raw.get("ownerName", "")
    return {
        "slug": slug,
        "name": raw.get("name", ""),
        "description": raw.get("description") or raw.get("description_zh") or "",
        "description_zh": raw.get("description_zh") or "",
        "categories": _flatten_tags_list([raw.get("category")] if raw.get("category") else []),
        "tags": _flatten_tags_list(raw.get("subCategories") or []),
        "installs": _safe_int(raw.get("installs") or raw.get("installsCount")),
        "downloads": _safe_int(raw.get("downloads")),
        "stars": _safe_int(raw.get("stars")),
        "ratings_count": _safe_int(raw.get("ratingsCount")),
        "versions_count": _safe_int(raw.get("versionCount") or raw.get("versions_count")),
        "created_at": _to_iso(raw.get("created_at") or raw.get("createdAt")),
        "updated_at": _to_iso(raw.get("updated_at") or raw.get("updatedAt")),
        "owner": owner,
        "verified": bool(raw.get("verified")),
        "has_changelog": bool(raw.get("latestChangelog") or raw.get("changelog")),
        "latest_changelog": raw.get("latestChangelog") or raw.get("changelog"),
        "source_url": raw.get("homepage") or f"https://skillhub.cn/skills/{slug}",
    }


def merge(clawhub_path: Path, skillhub_path: Path, output_path: Path) -> dict:
    """合并两个快照为统一 schema。"""
    clawhub_data = json.loads(clawhub_path.read_text(encoding="utf-8"))
    skillhub_data = json.loads(skillhub_path.read_text(encoding="utf-8"))

    clawhub_skills = clawhub_data.get("skills", [])
    skillhub_skills = skillhub_data.get("skills", [])

    # 用 normalized slug 作为合并键
    clawhub_map: dict[str, dict] = {}
    for raw in clawhub_skills:
        # ClawHub 数据是嵌套结构：raw.skill.slug
        skill_obj = raw.get("skill") or raw
        norm = _slug_normalize(skill_obj.get("slug", ""))
        if norm:
            clawhub_map[norm] = _normalize_clawhub(raw)

    skillhub_map: dict[str, dict] = {}
    for raw in skillhub_skills:
        norm = _slug_normalize(raw.get("slug", ""))
        if norm:
            skillhub_map[norm] = _normalize_skillhub(raw)

    all_keys = set(clawhub_map.keys()) | set(skillhub_map.keys())

    merged_skills = []
    for key in all_keys:
        ch = clawhub_map.get(key)
        sh = skillhub_map.get(key)

        if ch and sh:
            source = "both"
        elif ch:
            source = "clawhub"
        else:
            source = "skillhub"

        # 统一字段
        base = ch or sh
        unified = {
            "slug": base.get("slug", ""),
            "name": base.get("name", ""),
            "description": (ch.get("description") if ch else "") + (
                "\n\n" + sh.get("description_zh") if sh and sh.get("description_zh") else ""
            ).strip(),
            "categories": list(set((ch.get("categories") if ch else []) + (sh.get("categories") if sh else []))),
            "tags": list(set((ch.get("tags") if ch else []) + (sh.get("tags") if sh else []))),
            "installs": {
                "clawhub": ch["installs"] if ch else 0,
                "skillhub": sh["installs"] if sh else 0,
                "total": (ch["installs"] if ch else 0) + (sh["installs"] if sh else 0),
            },
            "stars": {
                "clawhub": ch["stars"] if ch else 0,
                "skillhub": sh["stars"] if sh else 0,
                "total": (ch["stars"] if ch else 0) + (sh["stars"] if sh else 0),
            },
            "downloads": {
                "clawhub": ch["downloads"] if ch else 0,
                "skillhub": sh["downloads"] if sh else 0,
                "total": (ch["downloads"] if ch else 0) + (sh["downloads"] if sh else 0),
            },
            "versions_count": max(
                ch["versions_count"] if ch else 0,
                sh["versions_count"] if sh else 0,
            ),
            "created_at": min(
                filter(None, [
                    ch["created_at"] if ch else None,
                    sh["created_at"] if sh else None,
                ]),
                default=None,
            ),
            "updated_at": max(
                filter(None, [
                    ch["updated_at"] if ch else None,
                    sh["updated_at"] if sh else None,
                ]),
                default=None,
            ),
            "owner": (ch["owner"] if ch else "") or (sh["owner"] if sh else ""),
            "verified": (ch["verified"] if ch else False) or (sh["verified"] if sh else False),
            "has_changelog": (ch["has_changelog"] if ch else False) or (sh["has_changelog"] if sh else False),
            "latest_changelog": (ch["latest_changelog"] if ch else None) or (sh["latest_changelog"] if sh else None),
            "ratings_count": max(
                ch["ratings_count"] if ch else 0,
                sh["ratings_count"] if sh else 0,
            ),
            "platforms_active": (
                ["clawhub", "skillhub"] if source == "both"
                else ["clawhub"] if source == "clawhub"
                else ["skillhub"]
            ),
        }

        # 时间字段
        unified["age_days"] = _age_days(unified["created_at"])
        unified["days_since_update"] = _age_days(unified["updated_at"])

        # 速率指标
        age = max(unified["age_days"] or 1, 1)
        unified["install_rate"] = unified["installs"]["total"] / age
        unified["star_rate"] = (
            unified["stars"]["total"] / unified["downloads"]["total"] * 100
            if unified["downloads"]["total"] > 0
            else 0.0
        )

        # 跨平台差距比（独占维度用）
        ch_installs = unified["installs"]["clawhub"]
        sh_installs = unified["installs"]["skillhub"]
        if ch_installs == 0 and sh_installs == 0:
            unified["platform_gap_ratio"] = 1.0
        elif ch_installs == 0:
            unified["platform_gap_ratio"] = float("inf")  # 国内独火
        elif sh_installs == 0:
            unified["platform_gap_ratio"] = 0.0  # 全球独火
        else:
            unified["platform_gap_ratio"] = sh_installs / ch_installs

        merged_skills.append({
            "slug": unified["slug"],
            "name": unified["name"],
            "source": source,
            "clawhub": ch,
            "skillhub": sh,
            "unified": unified,
        })

    # 按总安装量降序
    merged_skills.sort(
        key=lambda x: x["unified"]["installs"]["total"],
        reverse=True,
    )

    result = {
        "snapshot_date": clawhub_data.get("snapshot_date") or skillhub_data.get("snapshot_date") or datetime.now().strftime("%Y-%m-%d"),
        "fetched_at": datetime.now(tz=timezone.utc).isoformat(),
        "clawhub_count": len(clawhub_skills),
        "skillhub_count": len(skillhub_skills),
        "merged_count": len(merged_skills),
        "both_count": sum(1 for s in merged_skills if s["source"] == "both"),
        "clawhub_only_count": sum(1 for s in merged_skills if s["source"] == "clawhub"),
        "skillhub_only_count": sum(1 for s in merged_skills if s["source"] == "skillhub"),
        "skills": merged_skills,
    }

    output_path.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    return result


def main():
    if len(sys.argv) < 4:
        print("Usage: python normalize.py <clawhub.json> <skillhub.json> <output.json>")
        sys.exit(1)

    clawhub_path = Path(sys.argv[1])
    skillhub_path = Path(sys.argv[2])
    output_path = Path(sys.argv[3])

    if not clawhub_path.exists():
        print(f"[normalize] ClawHub snapshot not found: {clawhub_path}")
        sys.exit(1)
    if not skillhub_path.exists():
        print(f"[normalize] SkillHub snapshot not found: {skillhub_path}")
        sys.exit(1)

    result = merge(clawhub_path, skillhub_path, output_path)
    print(f"[normalize] merged: clawhub={result['clawhub_count']} + skillhub={result['skillhub_count']} → {result['merged_count']} (both={result['both_count']}, clawhub_only={result['clawhub_only_count']}, skillhub_only={result['skillhub_only_count']})")
    print(f"[normalize] output: {output_path}")


if __name__ == "__main__":
    main()
