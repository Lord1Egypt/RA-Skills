from __future__ import annotations

from collections import defaultdict
import re
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any

from .config import AppConfig
from .db import get_mal_anime_metadata_map, get_mal_anime_relations_map, get_mal_recommendation_edges_map, list_series_mappings
from .mapping import normalize_title
from .sync_planner import ProviderSeriesState, load_provider_series_states

_ENGLISH_DUB_RE = re.compile(r"\benglish dub\b|\(dub\)", re.IGNORECASE)
_FOREIGN_DUB_RE = re.compile(r"\b(?:french|german|spanish|portuguese|italian|arabic|hindi) dub\b", re.IGNORECASE)
_SEASON_NUMBER_RE = re.compile(r"\bseason\s*(\d+)\b", re.IGNORECASE)
_ORDINAL_SEASON_RE = re.compile(
    r"\b(first|second|third|fourth|fifth|sixth|seventh|eighth|ninth|tenth|\d+(?:st|nd|rd|th))\s+season\b",
    re.IGNORECASE,
)
_FINAL_SEASON_RE = re.compile(r"\bfinal\s+season\b", re.IGNORECASE)
_PART_RE = re.compile(r"\bpart\s*(\d+)\b", re.IGNORECASE)
_ROMAN_END_RE = re.compile(r"\b([ivx]{1,5})\b(?=\s*(?:\(|$))", re.IGNORECASE)

_ORDINALS = {
    "first": 1,
    "second": 2,
    "third": 3,
    "fourth": 4,
    "fifth": 5,
    "sixth": 6,
    "seventh": 7,
    "eighth": 8,
    "ninth": 9,
    "tenth": 10,
}

_ROMAN = {
    "i": 1,
    "ii": 2,
    "iii": 3,
    "iv": 4,
    "v": 5,
    "vi": 6,
    "vii": 7,
    "viii": 8,
    "ix": 9,
    "x": 10,
}

_FRESH_DUBBED_EPISODE_WINDOW_DAYS = 21


@dataclass(slots=True)
class Recommendation:
    kind: str
    priority: int
    provider_series_id: str
    title: str
    season_title: str | None
    reasons: list[str] = field(default_factory=list)
    context: dict[str, Any] = field(default_factory=dict)

    def as_dict(self) -> dict[str, Any]:
        return {
            "kind": self.kind,
            "priority": self.priority,
            "provider_series_id": self.provider_series_id,
            "title": self.title,
            "season_title": self.season_title,
            "reasons": self.reasons,
            "context": self.context,
        }


@dataclass(slots=True, frozen=True)
class RecommendationSectionDefinition:
    key: str
    title: str
    kinds: tuple[str, ...]
    description: str


_RECOMMENDATION_SECTIONS: tuple[RecommendationSectionDefinition, ...] = (
    RecommendationSectionDefinition(
        key="continue_next",
        title="Continue next",
        kinds=("new_season",),
        description="Later-season continuations that look ready because an earlier installment appears completed.",
    ),
    RecommendationSectionDefinition(
        key="fresh_dubbed_episodes",
        title="Fresh dubbed episodes",
        kinds=("new_dubbed_episode",),
        description="Recent contiguous tail gaps that look like actual new dubbed episode availability.",
    ),
    RecommendationSectionDefinition(
        key="discovery_candidates",
        title="Discovery candidates",
        kinds=("discovery_candidate",),
        description="Unmapped titles supported by cached MAL recommendation-graph evidence.",
    ),
    RecommendationSectionDefinition(
        key="resume_backlog",
        title="Resume backlog",
        kinds=("resume_backlog",),
        description="Older tail gaps that look more like backlog continuation than fresh release alerts.",
    ),
)


def group_recommendations(items: list[Recommendation]) -> list[dict[str, Any]]:
    items_by_kind: dict[str, list[Recommendation]] = defaultdict(list)
    for item in items:
        items_by_kind[item.kind].append(item)

    sections: list[dict[str, Any]] = []
    consumed_kinds: set[str] = set()
    for section in _RECOMMENDATION_SECTIONS:
        section_items: list[Recommendation] = []
        for kind in section.kinds:
            section_items.extend(items_by_kind.get(kind, []))
            consumed_kinds.add(kind)
        if not section_items:
            continue
        section_items.sort(key=lambda item: (-item.priority, item.title.lower(), item.provider_series_id))
        sections.append(
            {
                "key": section.key,
                "title": section.title,
                "description": section.description,
                "kinds": list(section.kinds),
                "count": len(section_items),
                "items": [item.as_dict() for item in section_items],
            }
        )

    remaining_items: list[Recommendation] = []
    for item in items:
        if item.kind not in consumed_kinds:
            remaining_items.append(item)
    if remaining_items:
        remaining_items.sort(key=lambda item: (-item.priority, item.title.lower(), item.provider_series_id))
        sections.append(
            {
                "key": "other",
                "title": "Other",
                "description": "Recommendation kinds that do not yet have a dedicated named section.",
                "kinds": sorted({item.kind for item in remaining_items}),
                "count": len(remaining_items),
                "items": [item.as_dict() for item in remaining_items],
            }
        )
    return sections


def build_recommendations(config: AppConfig, limit: int | None = 20) -> list[Recommendation]:
    states = load_provider_series_states(config, limit=None)
    state_by_id = {state.provider_series_id: state for state in states}
    mapping_by_series = {
        mapping.provider_series_id: int(mapping.mal_anime_id)
        for mapping in list_series_mappings(config.db_path, provider="crunchyroll", approved_only=False)
    }
    metadata_by_id = get_mal_anime_metadata_map(config.db_path)
    relations_by_id = get_mal_anime_relations_map(config.db_path)
    recommendation_edges_by_id = get_mal_recommendation_edges_map(config.db_path)

    recommendations: list[Recommendation] = []
    recommendations.extend(
        _build_relation_backed_new_season_recommendations(
            states,
            state_by_id=state_by_id,
            mapping_by_series=mapping_by_series,
            metadata_by_id=metadata_by_id,
            relations_by_id=relations_by_id,
        )
    )
    recommendations.extend(_build_new_season_recommendations(states))
    recommendations.extend(
        _build_discovery_recommendations(
            states,
            mapping_by_series=mapping_by_series,
            metadata_by_id=metadata_by_id,
            relations_by_id=relations_by_id,
            recommendation_edges_by_id=recommendation_edges_by_id,
        )
    )
    recommendations.extend(_build_new_episode_recommendations(states))
    recommendations = _dedupe_recommendations(recommendations)
    recommendations.sort(key=lambda item: (-item.priority, item.title.lower(), item.provider_series_id))
    if limit is None or limit <= 0:
        return recommendations
    return recommendations[:limit]


def _build_new_episode_recommendations(states: list[ProviderSeriesState]) -> list[Recommendation]:
    items: list[Recommendation] = []
    for state in states:
        if not _is_english_dub_series(state):
            continue
        if state.completed_episode_count <= 0:
            continue
        if state.max_episode_number is None:
            continue

        tail_gap = _contiguous_tail_gap(state)
        if tail_gap is None or tail_gap <= 0:
            continue

        days_since_watch = _days_since(state.last_watched_at)
        is_recent = days_since_watch is not None and days_since_watch <= _FRESH_DUBBED_EPISODE_WINDOW_DAYS
        kind = "new_dubbed_episode" if is_recent else "resume_backlog"
        reasons = [
            "English dub is available",
            f"{tail_gap} contiguous episode(s) appear beyond your completed tail progress",
        ]
        if kind == "resume_backlog":
            reasons.append("this looks more like a backlog continuation than a fresh release alert")
        if state.last_watched_at:
            reasons.append(f"most recent watch activity: {state.last_watched_at}")
        priority = _episode_recommendation_priority(state, tail_gap, kind)
        items.append(
            Recommendation(
                kind=kind,
                priority=priority,
                provider_series_id=state.provider_series_id,
                title=state.title,
                season_title=state.season_title,
                reasons=reasons,
                context={
                    "completed_episode_count": state.completed_episode_count,
                    "max_episode_number": state.max_episode_number,
                    "max_completed_episode_number": state.max_completed_episode_number,
                    "contiguous_tail_gap": tail_gap,
                    "watchlist_status": state.watchlist_status,
                    "last_watched_at": state.last_watched_at,
                    "days_since_last_watch": days_since_watch,
                },
            )
        )
    return items


def _contiguous_tail_gap(state: ProviderSeriesState) -> int | None:
    if state.max_episode_number is None or state.max_completed_episode_number is None:
        return None
    if state.max_completed_episode_number >= state.max_episode_number:
        return None
    if state.completed_episode_count != state.max_completed_episode_number:
        return None
    return state.max_episode_number - state.max_completed_episode_number


def _episode_recommendation_priority(state: ProviderSeriesState, tail_gap: int, kind: str) -> int:
    base = 55 if kind == "new_dubbed_episode" else 30
    priority = base - min(tail_gap, 10)
    if tail_gap == 1:
        priority += 10
    if state.watchlist_status == "in_progress":
        priority += 12
    elif state.watchlist_status == "fully_watched":
        priority -= 20
    priority += _freshness_boost(state.last_watched_at, kind)
    return priority


def _days_since(last_watched_at: str | None) -> int | None:
    if not last_watched_at:
        return None
    try:
        watched = datetime.fromisoformat(last_watched_at.replace("Z", "+00:00"))
    except ValueError:
        return None
    now = datetime.now(timezone.utc)
    return max((now - watched).days, 0)


def _freshness_boost(last_watched_at: str | None, kind: str) -> int:
    days = _days_since(last_watched_at)
    if days is None:
        return -8 if kind == "new_dubbed_episode" else -2
    if days <= 7:
        return 10 if kind == "new_dubbed_episode" else 3
    if days <= 30:
        return 6 if kind == "new_dubbed_episode" else 1
    if days <= 90:
        return 2 if kind == "new_dubbed_episode" else 0
    if days <= 365:
        return -4 if kind == "new_dubbed_episode" else -2
    return -12 if kind == "new_dubbed_episode" else -4


def _dedupe_recommendations(items: list[Recommendation]) -> list[Recommendation]:
    best: dict[tuple[str, str], Recommendation] = {}
    for item in items:
        key = (item.kind, item.provider_series_id)
        existing = best.get(key)
        if existing is None or item.priority > existing.priority:
            best[key] = item
    return list(best.values())


def _metadata_named_list_values(meta: Any, field: str) -> set[str]:
    if meta is None or not isinstance(getattr(meta, "raw", None), dict):
        return set()
    values: set[str] = set()
    for item in meta.raw.get(field) or []:
        if not isinstance(item, dict):
            continue
        name = item.get("name")
        if isinstance(name, str) and name.strip():
            values.add(name.strip())
    return values


def _metadata_genre_names(meta: Any) -> set[str]:
    return _metadata_named_list_values(meta, "genres")


def _metadata_studio_names(meta: Any) -> set[str]:
    return _metadata_named_list_values(meta, "studios")


def _metadata_source_value(meta: Any) -> str | None:
    raw = meta.raw if meta is not None and isinstance(getattr(meta, "raw", None), dict) else None
    value = raw.get("source") if isinstance(raw, dict) else None
    if not isinstance(value, str):
        return None
    value = value.strip()
    return value or None


def _normalized_title_aliases(*values: str | None) -> set[str]:
    aliases: set[str] = set()
    for value in values:
        if not isinstance(value, str):
            continue
        normalized = normalize_title(value)
        if normalized:
            aliases.add(normalized)
    return aliases


def _metadata_title_aliases(meta: Any) -> set[str]:
    if meta is None:
        return set()
    raw = meta.raw if isinstance(getattr(meta, "raw", None), dict) else {}
    aliases = _normalized_title_aliases(
        getattr(meta, "title", None),
        getattr(meta, "title_english", None),
        getattr(meta, "title_japanese", None),
    )
    for alt in getattr(meta, "alternative_titles", []) or []:
        aliases.update(_normalized_title_aliases(alt))
    if isinstance(raw, dict):
        alternative_titles = raw.get("alternative_titles")
        if isinstance(alternative_titles, dict):
            aliases.update(_normalized_title_aliases(alternative_titles.get("en"), alternative_titles.get("ja")))
            synonyms = alternative_titles.get("synonyms")
            if isinstance(synonyms, list):
                for synonym in synonyms:
                    aliases.update(_normalized_title_aliases(synonym))
    return aliases


def _provider_catalog_title_aliases(states: list[ProviderSeriesState]) -> set[str]:
    aliases: set[str] = set()
    for state in states:
        aliases.update(_normalized_title_aliases(state.title, state.season_title))
    return aliases


_DISCOVERY_FRANCHISE_RELATION_TYPES = frozenset(
    {
        "sequel",
        "prequel",
        "parent_story",
        "side_story",
        "alternative_setting",
        "alternative_version",
        "spin_off",
        "summary",
        "full_story",
    }
)


def _build_discovery_recommendations(
    states: list[ProviderSeriesState],
    *,
    mapping_by_series: dict[str, int],
    metadata_by_id: dict[int, Any],
    relations_by_id: dict[int, list[Any]],
    recommendation_edges_by_id: dict[int, list[Any]],
) -> list[Recommendation]:
    seed_weights: dict[int, int] = {}
    for state in states:
        mal_anime_id = mapping_by_series.get(state.provider_series_id)
        if mal_anime_id is None:
            continue
        if state.watchlist_status == "fully_watched":
            seed_weights[mal_anime_id] = 3
        elif state.watchlist_status == "in_progress" and (state.completed_episode_count >= 3 or _days_since(state.last_watched_at) in range(0, 91)):
            seed_weights[mal_anime_id] = 2

    seed_genre_weights: dict[str, int] = {}
    seed_studio_weights: dict[str, int] = {}
    seed_source_weights: dict[str, int] = {}
    for mal_anime_id, weight in seed_weights.items():
        meta = metadata_by_id.get(mal_anime_id)
        for genre in _metadata_genre_names(meta):
            seed_genre_weights[genre] = seed_genre_weights.get(genre, 0) + weight
        for studio in _metadata_studio_names(meta):
            seed_studio_weights[studio] = seed_studio_weights.get(studio, 0) + weight
        source = _metadata_source_value(meta)
        if source is not None:
            seed_source_weights[source] = seed_source_weights.get(source, 0) + weight

    candidate_scores: dict[int, dict[str, Any]] = {}
    watched_ids = set(seed_weights)
    mapped_ids = set(mapping_by_series.values())
    provider_catalog_aliases = _provider_catalog_title_aliases(states)
    direct_franchise_relation_targets_by_source: dict[int, set[int]] = {}
    globally_related_franchise_targets: set[int] = set()
    for source_id in seed_weights:
        direct_targets = {
            relation.related_mal_anime_id
            for relation in relations_by_id.get(source_id, [])
            if relation.relation_type in _DISCOVERY_FRANCHISE_RELATION_TYPES
        }
        direct_franchise_relation_targets_by_source[source_id] = direct_targets
        globally_related_franchise_targets.update(direct_targets)
    for source_id, weight in seed_weights.items():
        for edge in recommendation_edges_by_id.get(source_id, [])[:15]:
            target_id = edge.target_mal_anime_id
            if target_id in watched_ids or target_id in mapped_ids:
                continue
            if target_id in globally_related_franchise_targets:
                continue
            if target_id in direct_franchise_relation_targets_by_source.get(source_id, set()):
                continue
            bucket = candidate_scores.setdefault(
                target_id,
                {
                    "supporting_sources": set(),
                    "raw_score": 0.0,
                    "votes": 0,
                    "title": edge.target_title,
                },
            )
            votes = edge.num_recommendations or 0
            bucket["supporting_sources"].add(source_id)
            bucket["votes"] += votes
            bucket["raw_score"] += weight * min(votes, 40)

    items: list[Recommendation] = []
    for target_id, bucket in candidate_scores.items():
        meta = metadata_by_id.get(target_id)
        support_count = len(bucket["supporting_sources"])
        if support_count <= 0:
            continue
        if meta is not None and meta.media_type not in (None, "tv", "movie", "ova", "ona", "special"):
            continue
        if meta is not None:
            my_list_status = meta.raw.get("my_list_status") if isinstance(meta.raw, dict) else None
            if isinstance(my_list_status, dict):
                status_value = my_list_status.get("status")
                watched_count = my_list_status.get("num_episodes_watched")
                if status_value in {"completed", "watching", "on_hold", "dropped", "plan_to_watch"}:
                    continue
                if isinstance(watched_count, int) and watched_count > 0:
                    continue
        candidate_title_aliases = _metadata_title_aliases(meta)
        candidate_title_aliases.update(_normalized_title_aliases(bucket.get("title")))
        if candidate_title_aliases & provider_catalog_aliases:
            continue
        mean = meta.mean if meta is not None else None
        popularity = meta.popularity if meta is not None else None
        popularity_bonus = 0
        if popularity is not None:
            if popularity <= 100:
                popularity_bonus = 6
            elif popularity <= 500:
                popularity_bonus = 3
            elif popularity <= 2000:
                popularity_bonus = 1
        candidate_genres = _metadata_genre_names(meta)
        shared_genres = sorted(candidate_genres & set(seed_genre_weights), key=lambda genre: (-seed_genre_weights[genre], genre))
        genre_overlap_score = sum(seed_genre_weights[genre] for genre in shared_genres)
        genre_bonus = min(genre_overlap_score * 3, 18)
        candidate_studios = _metadata_studio_names(meta)
        shared_studios = sorted(candidate_studios & set(seed_studio_weights), key=lambda studio: (-seed_studio_weights[studio], studio))
        studio_overlap_score = sum(seed_studio_weights[studio] for studio in shared_studios)
        studio_bonus = min(studio_overlap_score * 2, 10)
        candidate_source = _metadata_source_value(meta)
        source_overlap_score = seed_source_weights.get(candidate_source, 0) if candidate_source is not None else 0
        source_bonus = min(source_overlap_score * 2, 6)
        priority = int(min(bucket["raw_score"] / 8.0, 60)) + support_count * 12 + int(mean or 0)
        priority += popularity_bonus + genre_bonus + studio_bonus + source_bonus
        reasons = [
            f"recommended by {support_count} watched/mapped seed title(s)",
        ]
        if bucket["votes"]:
            reasons.append(f"aggregated MAL recommendation votes: {bucket['votes']}")
        if shared_genres:
            reasons.append("shared seed genres: " + ", ".join(shared_genres[:3]))
        if shared_studios:
            reasons.append("shared seed studios: " + ", ".join(shared_studios[:2]))
        if source_overlap_score > 0 and candidate_source is not None:
            reasons.append(f"shared seed source material: {candidate_source}")
        if mean is not None:
            reasons.append(f"MAL mean score: {mean}")
        if meta is None:
            reasons.append("full MAL metadata for this discovery candidate is not cached yet")
        title = meta.title if meta is not None else (bucket.get("title") or f"MAL anime {target_id}")
        items.append(
            Recommendation(
                kind="discovery_candidate",
                priority=priority,
                provider_series_id=f"mal:{target_id}",
                title=title,
                season_title=None,
                reasons=reasons,
                context={
                    "mal_anime_id": target_id,
                    "supporting_source_count": support_count,
                    "supporting_mal_anime_ids": sorted(bucket["supporting_sources"]),
                    "aggregated_recommendation_votes": bucket["votes"],
                    "shared_genres": shared_genres,
                    "genre_overlap_score": genre_overlap_score,
                    "shared_studios": shared_studios,
                    "studio_overlap_score": studio_overlap_score,
                    "source": candidate_source,
                    "source_overlap_score": source_overlap_score,
                    "mean": mean,
                    "popularity": popularity,
                    "media_type": meta.media_type if meta is not None else None,
                    "num_episodes": meta.num_episodes if meta is not None else None,
                    "metadata_cached": meta is not None,
                },
            )
        )
    return items


def _build_relation_backed_new_season_recommendations(
    states: list[ProviderSeriesState],
    *,
    state_by_id: dict[str, ProviderSeriesState],
    mapping_by_series: dict[str, int],
    metadata_by_id: dict[int, Any],
    relations_by_id: dict[int, list[Any]],
) -> list[Recommendation]:
    items: list[Recommendation] = []
    series_by_anime_id = {anime_id: state_by_id[sid] for sid, anime_id in mapping_by_series.items() if sid in state_by_id}
    sequel_relation_types = {"sequel"}
    predecessor_relation_types = {"prequel", "parent_story"}
    for state in states:
        current_anime_id = mapping_by_series.get(state.provider_series_id)
        if current_anime_id is None:
            continue
        if not _is_english_dub_series(state):
            continue
        relations = relations_by_id.get(current_anime_id, [])
        best_predecessor = None
        for relation in relations:
            if relation.relation_type not in predecessor_relation_types:
                continue
            predecessor_state = series_by_anime_id.get(relation.related_mal_anime_id)
            if predecessor_state is None or not _series_counts_as_completed(predecessor_state):
                continue
            best_predecessor = predecessor_state
            break
        if best_predecessor is not None and state.completed_episode_count <= 0:
            title_hint = metadata_by_id.get(current_anime_id).title if current_anime_id in metadata_by_id else state.title
            items.append(
                Recommendation(
                    kind="new_season",
                    priority=110,
                    provider_series_id=state.provider_series_id,
                    title=state.title,
                    season_title=state.season_title,
                    reasons=[
                        "English dub is available",
                        f"MAL relation metadata links this title as a continuation after {best_predecessor.season_title or best_predecessor.title}",
                    ],
                    context={
                        "relation_backed": True,
                        "mal_anime_id": current_anime_id,
                        "metadata_title": title_hint,
                        "predecessor_provider_series_id": best_predecessor.provider_series_id,
                        "predecessor_title": best_predecessor.season_title or best_predecessor.title,
                    },
                )
            )
            continue

        if state.completed_episode_count > 0:
            for relation in relations:
                if relation.relation_type not in sequel_relation_types:
                    continue
                sequel_state = series_by_anime_id.get(relation.related_mal_anime_id)
                if sequel_state is None or not _is_english_dub_series(sequel_state):
                    continue
                if sequel_state.completed_episode_count > 0:
                    continue
                title_hint = metadata_by_id.get(relation.related_mal_anime_id).title if relation.related_mal_anime_id in metadata_by_id else sequel_state.title
                items.append(
                    Recommendation(
                        kind="new_season",
                        priority=112,
                        provider_series_id=sequel_state.provider_series_id,
                        title=sequel_state.title,
                        season_title=sequel_state.season_title,
                        reasons=[
                            "English dub is available",
                            f"MAL relation metadata links this as a sequel to {state.season_title or state.title}",
                        ],
                        context={
                            "relation_backed": True,
                            "mal_anime_id": relation.related_mal_anime_id,
                            "metadata_title": title_hint,
                            "predecessor_provider_series_id": state.provider_series_id,
                            "predecessor_title": state.season_title or state.title,
                        },
                    )
                )
    return items


def _build_new_season_recommendations(states: list[ProviderSeriesState]) -> list[Recommendation]:
    items: list[Recommendation] = []
    by_franchise: dict[str, list[tuple[int, ProviderSeriesState]]] = {}
    for state in states:
        if not _is_english_dub_series(state):
            continue
        installment = _series_installment_index(state)
        if installment is None:
            continue
        key = normalize_title(state.title)
        if not key:
            continue
        by_franchise.setdefault(key, []).append((installment, state))

    for entries in by_franchise.values():
        entries.sort(key=lambda item: (item[0], item[1].title.lower(), item[1].provider_series_id))
        for installment, state in entries:
            if installment <= 1:
                continue
            predecessor = _find_best_completed_predecessor(entries, installment)
            if predecessor is None:
                continue
            if predecessor.provider_series_id == state.provider_series_id:
                continue
            reasons = [
                "English dub is available",
                f"a later season appears available after completing {predecessor.season_title or predecessor.title}",
            ]
            if state.watchlist_status:
                reasons.append(f"Crunchyroll watchlist status: {state.watchlist_status}")
            priority = 100 - min(max(installment - 1, 0), 10)
            if state.completed_episode_count <= 0:
                priority += 5
            items.append(
                Recommendation(
                    kind="new_season",
                    priority=priority,
                    provider_series_id=state.provider_series_id,
                    title=state.title,
                    season_title=state.season_title,
                    reasons=reasons,
                    context={
                        "installment_index": installment,
                        "predecessor_provider_series_id": predecessor.provider_series_id,
                        "predecessor_title": predecessor.season_title or predecessor.title,
                        "predecessor_completed_episode_count": predecessor.completed_episode_count,
                        "predecessor_max_episode_number": predecessor.max_episode_number,
                        "watchlist_status": state.watchlist_status,
                    },
                )
            )
    return items


def _find_best_completed_predecessor(
    entries: list[tuple[int, ProviderSeriesState]], current_installment: int
) -> ProviderSeriesState | None:
    best: tuple[int, ProviderSeriesState] | None = None
    for installment, state in entries:
        if installment >= current_installment:
            continue
        if not _series_counts_as_completed(state):
            continue
        if best is None or installment > best[0]:
            best = (installment, state)
    return None if best is None else best[1]


def _series_counts_as_completed(state: ProviderSeriesState) -> bool:
    if state.watchlist_status == "fully_watched":
        return True
    if state.max_episode_number is None or state.max_episode_number <= 0:
        return False
    return state.completed_episode_count >= state.max_episode_number


def _is_english_dub_series(state: ProviderSeriesState) -> bool:
    haystacks = [value for value in (state.season_title, state.title) if value]
    if not haystacks:
        return False
    joined = " ".join(haystacks)
    if _FOREIGN_DUB_RE.search(joined):
        return False
    return bool(_ENGLISH_DUB_RE.search(joined))


def _has_explicit_season_style_evidence(text: str) -> bool:
    return bool(
        _SEASON_NUMBER_RE.search(text) or _ORDINAL_SEASON_RE.search(text) or _FINAL_SEASON_RE.search(text)
    )


def _series_installment_index(state: ProviderSeriesState) -> int | None:
    candidates: list[int] = []
    if state.season_number is not None and state.season_number > 0:
        candidates.append(int(state.season_number))
    for text in (state.season_title, state.title):
        if not text:
            continue
        season_match = _SEASON_NUMBER_RE.search(text)
        if season_match:
            candidates.append(int(season_match.group(1)))
        ordinal_match = _ORDINAL_SEASON_RE.search(text)
        if ordinal_match:
            raw = ordinal_match.group(1).lower()
            if raw in _ORDINALS:
                candidates.append(_ORDINALS[raw])
            else:
                digits = re.sub(r"\D+", "", raw)
                if digits:
                    candidates.append(int(digits))
        part_match = _PART_RE.search(text)
        if part_match and _has_explicit_season_style_evidence(text):
            candidates.append(int(part_match.group(1)))
        roman_match = _ROMAN_END_RE.search(text)
        if roman_match:
            roman_value = _ROMAN.get(roman_match.group(1).lower())
            if roman_value:
                candidates.append(roman_value)
    positive = [value for value in candidates if value > 0]
    if positive:
        return max(positive)
    return 1 if (state.title or state.season_title) else None
