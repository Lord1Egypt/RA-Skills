from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(slots=True)
class _DiscoveredTargetStats:
    title: str | None = None
    supporting_sources: int = 0
    total_recommendation_votes: int = 0
    best_single_source_votes: int = 0

    def observe(self, *, title: str | None, num_recommendations: int) -> None:
        self.supporting_sources += 1
        if title and not self.title:
            self.title = title
        self.total_recommendation_votes += max(num_recommendations, 0)
        self.best_single_source_votes = max(self.best_single_source_votes, max(num_recommendations, 0))

from .config import AppConfig, load_mal_secrets
from .db import (
    list_series_mappings,
    replace_mal_anime_relations,
    replace_mal_recommendation_edges,
    upsert_mal_anime_metadata,
)
from .mal_client import MalClient

DETAIL_FIELDS = (
    "id,title,alternative_titles,media_type,status,num_episodes,mean,popularity,start_season,source,genres,studios,related_anime,recommendations,my_list_status"
)


@dataclass(slots=True)
class MetadataRefreshSummary:
    considered: int
    refreshed: int

    def as_dict(self) -> dict[str, Any]:
        return {"considered": self.considered, "refreshed": self.refreshed}


def refresh_recommendation_metadata(
    config: AppConfig,
    *,
    limit: int | None = None,
    include_discovery_targets: bool = False,
    discovery_target_limit: int | None = None,
) -> MetadataRefreshSummary:
    mappings = list_series_mappings(config.db_path, provider="crunchyroll", approved_only=False)
    anime_ids = sorted({int(mapping.mal_anime_id) for mapping in mappings})
    if limit is not None and limit > 0:
        anime_ids = anime_ids[:limit]

    client = MalClient(config, load_mal_secrets(config))
    refreshed = 0
    discovered_targets: dict[int, _DiscoveredTargetStats] = {}
    for anime_id in anime_ids:
        details = client.get_anime_details(anime_id, fields=DETAIL_FIELDS)
        alternative_titles = details.get("alternative_titles") or {}
        aliases: list[str] = []
        if isinstance(alternative_titles, dict):
            for key in ("en", "ja"):
                value = alternative_titles.get(key)
                if isinstance(value, str) and value.strip():
                    aliases.append(value.strip())
            synonyms = alternative_titles.get("synonyms")
            if isinstance(synonyms, list):
                for value in synonyms:
                    if isinstance(value, str) and value.strip():
                        aliases.append(value.strip())

        upsert_mal_anime_metadata(
            config.db_path,
            mal_anime_id=anime_id,
            title=str(details.get("title") or anime_id),
            title_english=alternative_titles.get("en") if isinstance(alternative_titles, dict) else None,
            title_japanese=alternative_titles.get("ja") if isinstance(alternative_titles, dict) else None,
            alternative_titles=aliases,
            media_type=str(details.get("media_type")) if details.get("media_type") else None,
            status=str(details.get("status")) if details.get("status") else None,
            num_episodes=int(details["num_episodes"]) if isinstance(details.get("num_episodes"), int) else None,
            mean=float(details["mean"]) if isinstance(details.get("mean"), (float, int)) else None,
            popularity=int(details["popularity"]) if isinstance(details.get("popularity"), int) else None,
            start_season=details.get("start_season") if isinstance(details.get("start_season"), dict) else None,
            raw=details,
        )
        relations_payload: list[dict[str, Any]] = []
        for relation in details.get("related_anime") or []:
            if not isinstance(relation, dict):
                continue
            node = relation.get("node") or {}
            if not isinstance(node, dict) or not isinstance(node.get("id"), int):
                continue
            relation_type = relation.get("relation_type")
            if not isinstance(relation_type, str) or not relation_type:
                continue
            relations_payload.append(
                {
                    "related_mal_anime_id": int(node["id"]),
                    "relation_type": relation_type,
                    "relation_type_formatted": relation.get("relation_type_formatted"),
                    "related_title": node.get("title") if isinstance(node.get("title"), str) else None,
                    "raw": relation,
                }
            )
        replace_mal_anime_relations(config.db_path, mal_anime_id=anime_id, relations=relations_payload)

        recommendation_edges: list[dict[str, Any]] = []
        for rec in details.get("recommendations") or []:
            if not isinstance(rec, dict):
                continue
            node = rec.get("node") or {}
            if not isinstance(node, dict) or not isinstance(node.get("id"), int):
                continue
            target_id = int(node["id"])
            target_title = node.get("title") if isinstance(node.get("title"), str) else None
            num_recs = int(rec["num_recommendations"]) if isinstance(rec.get("num_recommendations"), int) else 0
            recommendation_edges.append(
                {
                    "target_mal_anime_id": target_id,
                    "target_title": target_title,
                    "num_recommendations": num_recs if num_recs > 0 else None,
                    "raw": rec,
                }
            )
            discovered_targets.setdefault(target_id, _DiscoveredTargetStats()).observe(
                title=target_title,
                num_recommendations=num_recs,
            )
        replace_mal_recommendation_edges(
            config.db_path,
            source_mal_anime_id=anime_id,
            hop_distance=1,
            edges=recommendation_edges,
        )
        refreshed += 1

    if include_discovery_targets and discovered_targets:
        ranked_targets = sorted(
            discovered_targets.items(),
            key=lambda item: (
                -item[1].supporting_sources,
                -item[1].total_recommendation_votes,
                -item[1].best_single_source_votes,
                item[0],
            ),
        )
        if discovery_target_limit is not None and discovery_target_limit > 0:
            ranked_targets = ranked_targets[:discovery_target_limit]
        for target_id, _info in ranked_targets:
            details = client.get_anime_details(
                target_id,
                fields="id,title,alternative_titles,media_type,status,num_episodes,mean,popularity,start_season,source,genres,studios,my_list_status",
            )
            alternative_titles = details.get("alternative_titles") or {}
            aliases: list[str] = []
            if isinstance(alternative_titles, dict):
                for key in ("en", "ja"):
                    value = alternative_titles.get(key)
                    if isinstance(value, str) and value.strip():
                        aliases.append(value.strip())
                synonyms = alternative_titles.get("synonyms")
                if isinstance(synonyms, list):
                    for value in synonyms:
                        if isinstance(value, str) and value.strip():
                            aliases.append(value.strip())
            upsert_mal_anime_metadata(
                config.db_path,
                mal_anime_id=target_id,
                title=str(details.get("title") or target_id),
                title_english=alternative_titles.get("en") if isinstance(alternative_titles, dict) else None,
                title_japanese=alternative_titles.get("ja") if isinstance(alternative_titles, dict) else None,
                alternative_titles=aliases,
                media_type=str(details.get("media_type")) if details.get("media_type") else None,
                status=str(details.get("status")) if details.get("status") else None,
                num_episodes=int(details["num_episodes"]) if isinstance(details.get("num_episodes"), int) else None,
                mean=float(details["mean"]) if isinstance(details.get("mean"), (float, int)) else None,
                popularity=int(details["popularity"]) if isinstance(details.get("popularity"), int) else None,
                start_season=details.get("start_season") if isinstance(details.get("start_season"), dict) else None,
                raw=details,
            )
    return MetadataRefreshSummary(considered=len(anime_ids), refreshed=refreshed)
