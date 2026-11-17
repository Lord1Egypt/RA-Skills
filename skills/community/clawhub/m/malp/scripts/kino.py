#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from collections import Counter
from datetime import datetime, timezone
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable

DOCTRINE_FILES = ("README.md", "STATUS.md", "DESIGN-RULES.md", "AGENTS.md")
SKIP_DIRS = {".git", "node_modules", "dist", "bin", "obj", ".next", ".angular", "coverage"}

STOPWORDS = {
    "a", "an", "and", "are", "as", "at", "be", "but", "by", "for", "from", "has", "have",
    "how", "if", "in", "into", "is", "it", "its", "may", "might", "more", "need", "not", "of",
    "on", "or", "our", "out", "should", "so", "than", "that", "the", "their", "them", "then",
    "there", "these", "they", "this", "to", "up", "use", "using", "want", "was", "we", "what",
    "when", "which", "who", "why", "with", "work", "working", "would", "you", "your",
    "malp", "malps", "kino", "context", "load", "loading", "recommendation", "question", "current",
    "reference", "references", "another", "similar", "maybe", "should", "helpful", "useful", "about",
    "anthony", "projects", "project", "workspace", "app", "area", "because", "before", "actual",
    "does", "any", "know", "knows", "support", "added", "first", "come", "related", "next",
    "bring", "lookup", "lookups", "query", "queries", "find", "finding",
}

LOW_SIGNAL_QUERY_WORDS = {
    "term", "topic", "issue", "issues", "problem", "problems", "question", "questions", "task",
    "tasks", "thing", "things", "stuff", "about", "around", "regarding",
}

COMMON_TERM_DF_THRESHOLD = 8
COMMON_TERM_MIN_LEN = 6

TEXT_FILES = ("SUMMARY.txt", "FOB.txt", "NOTES.txt")
CROSS_REF_RE = re.compile(r"(?P<path>(?:/[^\s`]+|\.\.?/[^\s`]+)[^\s`]*?/\.malp)")
TOKEN_RE = re.compile(r"[A-Za-z0-9_./:-]+")
PATH_PART_RE = re.compile(r"[A-Za-z0-9][A-Za-z0-9._-]+")
PROVENANCE_WORDS = {"who", "first", "added", "introduce", "introduced", "author", "authored", "history", "origin", "commit"}
PROVENANCE_SIGNAL_PHRASES = ("added by", "introduced by", "authored by", "first added", "commit ", "committed ")
QUERY_META_WORDS = {"does", "any", "know", "knows", "support", "added", "first", "who", "tres"}
GIT_NOISE_TERMS = {"api", "support"}
CONTAINMENT_META_WORDS = {"strictly", "contained", "containment", "group", "tags", "tag"}


@dataclass
class Candidate:
    path: Path
    state: str
    source: str
    score: float = 0.0
    reasons: list[str] = field(default_factory=list)
    summary: str = ""
    fob: str = ""
    notes_head: str = ""
    territory_head: str = ""
    cross_refs: list[str] = field(default_factory=list)
    exists: bool = False

    @property
    def root(self) -> Path:
        return self.path.parent

    @property
    def label(self) -> str:
        return str(self.path)


@dataclass
class GitFinding:
    repo: Path
    matched_term: str
    commit: str
    author: str
    date: str
    subject: str


@dataclass
class GitFreshness:
    status: str
    repo: str | None
    territory: str
    last_malp_update: str | None
    last_territory_commit: str | None
    commits_since_malp: int | None
    dirty: bool | None


@dataclass
class ContainmentReport:
    status: str
    term: str
    cluster_tags: list[str]
    supporting_malps: list[str]
    outside_hits: list[str]


def tokenize(text: str) -> set[str]:
    tokens: set[str] = set()
    for raw in TOKEN_RE.findall(text.lower()):
        piece = raw.strip("._-:/")
        if len(piece) < 3 or piece in STOPWORDS or piece.isdigit():
            continue
        tokens.add(piece)
        for sub in re.split(r"[./:_-]+", piece):
            if len(sub) >= 3 and sub not in STOPWORDS and not sub.isdigit():
                tokens.add(sub)
    return tokens


def cap_overlap(tokens: list[str], limit: int = 5) -> list[str]:
    filtered = [t for t in tokens if t not in STOPWORDS]
    return filtered[:limit]


def filter_question_terms(question_tokens: set[str], term_df: dict[str, int] | None = None) -> set[str]:
    base_tokens = {
        token for token in question_tokens
        if token not in STOPWORDS and token not in LOW_SIGNAL_QUERY_WORDS
    }
    if not term_df:
        return base_tokens

    filtered: set[str] = set()
    suppressed: set[str] = set()
    for token in base_tokens:
        if term_df.get(token, 0) >= COMMON_TERM_DF_THRESHOLD and len(token) < COMMON_TERM_MIN_LEN:
            suppressed.add(token)
            continue
        filtered.add(token)

    if filtered:
        return filtered

    # If suppression would erase the whole query, keep the original subject terms.
    return base_tokens or suppressed


def slurp(path: Path, max_chars: int = 4000) -> str:
    try:
        text = path.read_text(encoding="utf-8", errors="ignore")
    except FileNotFoundError:
        return ""
    except IsADirectoryError:
        return ""
    return text[:max_chars]


def summarize_territory(root: Path, max_entries: int = 20) -> str:
    parts: list[str] = []
    if not root.is_dir():
        return ""
    names: list[str] = []
    try:
        for child in sorted(root.iterdir(), key=lambda p: p.name.lower()):
            if child.name.startswith('.') and child.name != '.malp':
                continue
            names.append(child.name + ('/' if child.is_dir() else ''))
            if len(names) >= max_entries:
                break
    except Exception:
        names = []
    if names:
        parts.append('entries: ' + ', '.join(names))
    for filename in DOCTRINE_FILES:
        text = slurp(root / filename, 1200)
        if text:
            parts.append(f'{filename}: ' + first_nonempty_lines(text, 6))
    return '\n'.join(parts)


def first_nonempty_lines(text: str, limit: int = 8) -> str:
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    return "\n".join(lines[:limit])


def parse_map(path: Path, state: str) -> list[Candidate]:
    if not path.exists():
        return []
    out: list[Candidate] = []
    for raw in path.read_text(encoding="utf-8", errors="ignore").splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        out.append(Candidate(path=Path(os.path.expanduser(line)), state=state, source=path.name))
    return out


def candidate_from_path(path: Path, state: str = "unindexed", source: str = "path") -> Candidate:
    p = path.expanduser()
    if p.name != ".malp":
        p = p / ".malp"
    return Candidate(path=p, state=state, source=source)


def hydrate(candidate: Candidate) -> Candidate:
    candidate.exists = candidate.path.is_dir()
    candidate.summary = slurp(candidate.path / "SUMMARY.txt", 2000)
    candidate.fob = slurp(candidate.path / "FOB.txt", 1200)
    notes = slurp(candidate.path / "NOTES.txt", 2500)
    candidate.notes_head = first_nonempty_lines(notes, 10)
    candidate.territory_head = summarize_territory(candidate.root)
    candidate.cross_refs = sorted(set(CROSS_REF_RE.findall(notes + "\n" + candidate.fob + "\n" + candidate.summary)))
    return candidate


def full_malp_text(candidate: Candidate, max_chars: int = 12000) -> str:
    return "\n".join([
        slurp(candidate.path / "SUMMARY.txt", max_chars),
        slurp(candidate.path / "FOB.txt", max_chars),
        slurp(candidate.path / "NOTES.txt", max_chars),
    ])


def infer_candidate_tags(candidate: Candidate) -> list[str]:
    tags: list[str] = []
    for part in candidate.root.parts:
        piece = part.lower()
        if piece.startswith('.'):
            continue
        for token in PATH_PART_RE.findall(piece):
            for sub in re.split(r"[._-]+", token):
                if len(sub) >= 3 and sub not in STOPWORDS:
                    tags.append(sub)
    return sorted(set(tags))


def build_candidates(active_map: Path, attic_map: Path, current: Path | None, path_hint: Path | None, include_attic: bool) -> dict[str, Candidate]:
    candidates: dict[str, Candidate] = {}
    for cand in parse_map(active_map, "active"):
        candidates[str(cand.path)] = cand
    if include_attic:
        for cand in parse_map(attic_map, "attic"):
            candidates.setdefault(str(cand.path), cand)
    if current:
        current_cand = candidate_from_path(current, source="current")
        current_key = str(current_cand.path)
        existing = candidates.get(current_key)
        if existing:
            existing.source = f"{existing.source},current"
        else:
            candidates[current_key] = current_cand
    if path_hint:
        hinted = candidate_from_path(path_hint, source="path")
        candidates.setdefault(str(hinted.path), hinted)
    for cand in list(candidates.values()):
        hydrate(cand)
    return candidates


def gather_unindexed_near(path_hint: Path | None, known: dict[str, Candidate], limit: int = 12) -> list[Candidate]:
    if not path_hint:
        return []
    root = path_hint.expanduser()
    if root.name == ".malp":
        root = root.parent
    if root.is_file():
        root = root.parent
    search_root = root if root.is_dir() else root.parent
    seen = set(known)
    found: list[Candidate] = []
    try:
        iterator = search_root.rglob(".malp")
    except Exception:
        return []
    for p in iterator:
        key = str(p)
        if key in seen:
            continue
        found.append(hydrate(Candidate(path=p, state="unindexed", source="nearby-scan")))
        seen.add(key)
        if len(found) >= limit:
            break
    return found


def score_candidate(candidate: Candidate, question_tokens: set[str], anchor_tokens: set[str], current_path: Path | None, term_df: dict[str, int] | None = None) -> None:
    telemetry_text = "\n".join([candidate.summary, candidate.fob, candidate.notes_head])
    territory_text = "\n".join([candidate.label, candidate.territory_head])
    telemetry_tokens = tokenize(telemetry_text)
    territory_tokens = tokenize(territory_text)
    full_telemetry_tokens = tokenize(full_malp_text(candidate))
    signal_question_tokens = filter_question_terms(question_tokens, term_df=term_df)
    signal_anchor_tokens = filter_question_terms(anchor_tokens)
    territory_overlap_q = sorted(signal_question_tokens & territory_tokens)
    telemetry_overlap_q = sorted(signal_question_tokens & telemetry_tokens)
    territory_overlap_anchor = sorted(signal_anchor_tokens & territory_tokens)
    telemetry_overlap_anchor = sorted(signal_anchor_tokens & telemetry_tokens)
    exact_question_hits = [t for t in signal_question_tokens if t in full_telemetry_tokens]
    rare_exact_hits = [t for t in exact_question_hits if term_df and term_df.get(t, 9999) <= 3]

    if territory_overlap_q:
        shown = cap_overlap(territory_overlap_q)
        candidate.score += min(5.0, len(shown) * 1.15)
        if shown:
            candidate.reasons.append("territory overlap: " + ", ".join(shown))
    if telemetry_overlap_q:
        shown = cap_overlap(telemetry_overlap_q)
        candidate.score += min(2.6, len(shown) * 0.55)
        if shown:
            candidate.reasons.append("telemetry overlap: " + ", ".join(shown))
    if exact_question_hits:
        shown = cap_overlap(sorted(exact_question_hits))
        candidate.score += min(6.0, len(shown) * 2.0)
        if shown:
            candidate.reasons.append("exact term hit: " + ", ".join(shown))
    if rare_exact_hits:
        shown = cap_overlap(sorted(rare_exact_hits))
        candidate.score += min(6.0, len(shown) * 2.5)
        if shown:
            candidate.reasons.append("rare exact hit: " + ", ".join(shown))
    if territory_overlap_anchor:
        shown = cap_overlap(territory_overlap_anchor)
        candidate.score += min(3.0, len(shown) * 0.6)
        if shown:
            candidate.reasons.append("territory pattern: " + ", ".join(shown))
    if telemetry_overlap_anchor:
        shown = cap_overlap(telemetry_overlap_anchor)
        candidate.score += min(1.4, len(shown) * 0.3)
        if shown:
            candidate.reasons.append("telemetry pattern: " + ", ".join(shown))

    if candidate.fob:
        candidate.score += 0.4
        candidate.reasons.append("has FOB")
    if candidate.summary:
        candidate.score += 0.2
    if candidate.notes_head:
        candidate.score += 0.2
    if candidate.territory_head:
        candidate.score += 0.4
        candidate.reasons.append("territory sampled")

    if candidate.state == "active":
        candidate.score += 1.0
        candidate.reasons.append("active malp")
    elif candidate.state == "unindexed":
        candidate.score -= 0.2
        candidate.reasons.append("unindexed")
    elif candidate.state == "attic":
        candidate.score -= 1.5
        candidate.reasons.append("attic")

    if current_path:
        current_root = current_path.parent if current_path.name == ".malp" else current_path
        try:
            common = os.path.commonpath([str(current_root), str(candidate.root)])
        except ValueError:
            common = ""
        if common and common not in ("/", str(Path.home())):
            candidate.score += 0.8
            candidate.reasons.append("near current worksite")
        if current_root == candidate.root:
            candidate.score -= 0.5
            candidate.reasons.append("same root as current")
        if current_path.name == ".malp" and candidate.path == current_path:
            candidate.score += 0.4
            candidate.reasons.append("current malp")

    if not candidate.exists:
        candidate.score -= 2.0
        candidate.reasons.append("path missing")


def confidence_from_gap(best: float, runner_up: float) -> str:
    if best < 1.5:
        return "low"
    gap = best - runner_up
    if best >= 4.5 and gap >= 1.0:
        return "high"
    if best >= 2.5:
        return "medium"
    return "low"


def question_requests_provenance(question: str) -> bool:
    words = set(re.findall(r"[a-z]+", question.lower()))
    return bool(words & PROVENANCE_WORDS)


def infer_subject_terms(question_tokens: set[str]) -> list[str]:
    terms = [t for t in question_tokens if t not in QUERY_META_WORDS]
    return sorted(terms, key=lambda t: (-len(t), t))[:5]


def has_direct_provenance_signal(candidates: list[Candidate], subject_terms: list[str]) -> bool:
    if not subject_terms:
        return False
    for cand in candidates:
        for line in full_malp_text(cand).lower().splitlines():
            if not any(term in line for term in subject_terms):
                continue
            if any(phrase in line for phrase in PROVENANCE_SIGNAL_PHRASES):
                return True
    return False


def candidate_matches_subject(candidate: Candidate, subject_terms: list[str]) -> bool:
    haystack = "\n".join([full_malp_text(candidate), candidate.territory_head, candidate.label]).lower()
    return any(term in haystack for term in subject_terms)


def infer_git_terms(subject_terms: list[str]) -> list[str]:
    terms = [t for t in subject_terms if t not in GIT_NOISE_TERMS]
    if not terms:
        terms = subject_terms[:]
    return terms[:3]


def find_git_root(path: Path) -> Path | None:
    current = path
    if current.is_file():
        current = current.parent
    for probe in [current, *current.parents]:
        if (probe / ".git").exists():
            return probe
    return None


def run_git_log(repo: Path, term: str, max_commits: int) -> list[GitFinding]:
    findings: list[GitFinding] = []
    variants = []
    for variant in (term, term.title(), term.upper()):
        if variant not in variants:
            variants.append(variant)
    for variant in variants:
        cmd = [
            "git", "-C", str(repo), "log", "--reverse",
            "--date=short", f"--max-count={max_commits}",
            "--pretty=format:%ad\t%an\t%h\t%s", f"-S{variant}", "--", ".",
        ]
        try:
            proc = subprocess.run(cmd, capture_output=True, text=True, check=False)
        except Exception:
            continue
        if proc.returncode != 0 or not proc.stdout.strip():
            continue
        for line in proc.stdout.splitlines():
            parts = line.split("\t", 3)
            if len(parts) != 4:
                continue
            date, author, commit, subject = parts
            findings.append(GitFinding(repo=repo, matched_term=term, commit=commit, author=author, date=date, subject=subject))
    return findings


def collect_repo_identifiers(repo: Path, term: str, max_hits: int = 6) -> list[str]:
    pattern = re.compile(rf"[A-Za-z0-9_]*{re.escape(term)}[A-Za-z0-9_]*", re.IGNORECASE)
    hits: list[str] = []
    seen: set[str] = set()
    for root, dirs, files in os.walk(repo):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS and not d.startswith('.')]
        for name in files:
            if name.startswith('.'):
                continue
            path = Path(root) / name
            try:
                if path.stat().st_size > 2_000_000:
                    continue
                text = path.read_text(encoding="utf-8", errors="ignore")
            except Exception:
                continue
            for match in pattern.findall(text):
                key = match.lower()
                if key in seen:
                    continue
                seen.add(key)
                hits.append(match)
                if len(hits) >= max_hits:
                    return hits
    return hits


def gather_git_auxiliary(ranked: list[Candidate], subject_terms: list[str], max_candidates: int, max_commits: int) -> GitFinding | None:
    seen_repos: set[str] = set()
    findings: list[GitFinding] = []
    git_terms = infer_git_terms(subject_terms)
    if not git_terms:
        return None
    for cand in ranked:
        if cand.score <= 0:
            continue
        if not candidate_matches_subject(cand, subject_terms):
            continue
        repo = find_git_root(cand.root)
        if not repo:
            continue
        repo_key = str(repo)
        if repo_key in seen_repos:
            continue
        seen_repos.add(repo_key)
        for term in git_terms:
            search_terms = [term, *collect_repo_identifiers(repo, term)]
            deduped: list[str] = []
            for search_term in search_terms:
                if search_term not in deduped:
                    deduped.append(search_term)
            for search_term in deduped[:6]:
                findings.extend(run_git_log(repo, search_term, max_commits))
        if len(seen_repos) >= max_candidates:
            break
    if not findings:
        return None
    findings.sort(key=lambda f: (f.date, len(f.matched_term), f.repo.as_posix(), f.commit))
    return findings[0]


def isoformat_utc(timestamp: float | None) -> str | None:
    if timestamp is None:
        return None
    return datetime.fromtimestamp(timestamp, tz=timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def latest_malp_mtime(candidate: Candidate) -> float | None:
    mtimes: list[float] = []
    for name in TEXT_FILES:
        path = candidate.path / name
        if path.exists():
            try:
                mtimes.append(path.stat().st_mtime)
            except Exception:
                continue
    return max(mtimes) if mtimes else None


def territory_relpath(repo: Path, territory: Path) -> str:
    try:
        rel = territory.relative_to(repo)
        return "." if str(rel) == "" else str(rel)
    except ValueError:
        return str(territory)


def territory_pathspecs(repo: Path, territory: Path) -> list[str]:
    rel = territory_relpath(repo, territory)
    if rel == ".":
        return [".", ":(exclude).malp"]
    return [rel, f":(exclude){rel}/.malp"]


def git_capture(repo: Path, args: list[str]) -> str | None:
    cmd = ["git", "-C", str(repo), *args]
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, check=False)
    except Exception:
        return None
    if proc.returncode != 0:
        return None
    return proc.stdout.strip()


def compute_git_freshness(candidate: Candidate) -> GitFreshness:
    repo = find_git_root(candidate.root)
    malp_update_ts = latest_malp_mtime(candidate)
    territory = str(candidate.root)
    if not repo:
        return GitFreshness(
            status="unknown",
            repo=None,
            territory=territory,
            last_malp_update=isoformat_utc(malp_update_ts),
            last_territory_commit=None,
            commits_since_malp=None,
            dirty=None,
        )

    rel = territory_relpath(repo, candidate.root)
    pathspecs = territory_pathspecs(repo, candidate.root)
    latest_commit = git_capture(repo, ["log", "-1", "--date=iso-strict", "--format=%cI", "--", *pathspecs])
    dirty_out = git_capture(repo, ["status", "--porcelain", "--", *pathspecs])
    dirty = bool(dirty_out) if dirty_out is not None else None

    commits_since: int | None = None
    if malp_update_ts is not None:
        since = datetime.fromtimestamp(malp_update_ts, tz=timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        count_out = git_capture(repo, ["rev-list", "--count", f"--since={since}", "HEAD", "--", *pathspecs])
        if count_out and count_out.isdigit():
            commits_since = max(0, int(count_out))

    if latest_commit is None:
        status = "unknown"
    elif commits_since is None:
        status = "unknown"
    elif commits_since == 0 and not dirty:
        status = "fresh"
    elif commits_since <= 3:
        status = "slightly-behind"
    else:
        status = "stale"

    return GitFreshness(
        status=status,
        repo=str(repo),
        territory=territory,
        last_malp_update=isoformat_utc(malp_update_ts),
        last_territory_commit=latest_commit or None,
        commits_since_malp=commits_since,
        dirty=dirty,
    )


def compute_containment(ranked: list[Candidate], subject_terms: list[str], limit: int = 8) -> ContainmentReport | None:
    terms = [t for t in subject_terms if t not in CONTAINMENT_META_WORDS]
    if not terms:
        return None
    term = terms[0]
    hits: list[tuple[Candidate, list[str]]] = []
    for cand in ranked:
        full_text = full_malp_text(cand).lower()
        if term not in full_text:
            continue
        tags = infer_candidate_tags(cand)
        hits.append((cand, tags))
        if len(hits) >= limit:
            break
    if not hits:
        return ContainmentReport(
            status="insufficient-signal",
            term=term,
            cluster_tags=[],
            supporting_malps=[],
            outside_hits=[],
        )

    tag_counter: Counter[str] = Counter()
    for _, tags in hits:
        tag_counter.update(tags)
    threshold = max(1, len(hits) - 1)
    cluster_tags = [tag for tag, count in tag_counter.most_common() if count >= threshold][:5]
    support = [str(c.path) for c, _ in hits[:4]]

    outside: list[str] = []
    if cluster_tags:
        cluster_set = set(cluster_tags)
        for cand, tags in hits:
            if not cluster_set.issubset(set(tags)):
                outside.append(str(cand.path))
    else:
        outside = [str(c.path) for c, _ in hits[1:4]]

    if len(hits) == 1:
        status = "strictly-contained"
    elif not outside and cluster_tags:
        status = "strictly-contained"
    elif cluster_tags and len(outside) <= max(1, len(hits) // 3):
        status = "mostly-contained"
    else:
        status = "not-contained"

    return ContainmentReport(
        status=status,
        term=term,
        cluster_tags=cluster_tags,
        supporting_malps=support,
        outside_hits=outside[:4],
    )


def make_recommendation(candidates: list[Candidate], current: Path | None) -> dict:
    ranked = sorted(candidates, key=lambda c: (-c.score, c.label))
    best = ranked[0] if ranked else None
    runner_score = ranked[1].score if len(ranked) > 1 else 0.0

    if not best:
        return {
            "action": "insufficient-signal",
            "promotion": "none",
            "confidence": "low",
            "recommended_malp": None,
            "reasons": ["no candidate malps found"],
        }

    confidence = confidence_from_gap(best.score, runner_score)
    current_malp = current if current and current.name == ".malp" else (current / ".malp" if current else None)
    territory_hits = sum(1 for r in best.reasons if r.startswith("territory "))
    telemetry_hits = sum(1 for r in best.reasons if r.startswith("telemetry "))

    if current_malp and best.path == current_malp and best.score >= 1.5:
        action = "stay-current"
        promotion = "working"
    elif best.state == "attic":
        action = "consider-load-attic"
        promotion = "reference" if territory_hits >= telemetry_hits else "working"
    elif best.exists:
        action = "load-malp"
        promotion = "reference" if territory_hits > telemetry_hits else "working"
    else:
        action = "send-new-malp"
        promotion = "working"

    return {
        "action": action,
        "promotion": promotion,
        "confidence": confidence,
        "recommended_malp": str(best.path) if action != "send-new-malp" else None,
        "recommended_path": str(best.root) if action == "send-new-malp" else None,
        "reasons": best.reasons[:5],
        "score": round(best.score, 2),
        "alternatives": [
            {
                "malp": str(c.path),
                "state": c.state,
                "score": round(c.score, 2),
                "reasons": c.reasons[:3],
                "promotion": "reference" if sum(1 for r in c.reasons if r.startswith("territory ")) > sum(1 for r in c.reasons if r.startswith("telemetry ")) else "working",
            }
            for c in ranked[1:4]
            if c.score > 0
        ],
    }


def infer_anchor_text(current: Candidate | None, path_hint: Path | None) -> str:
    bits: list[str] = []
    if current:
        bits.extend([current.summary, current.fob, current.notes_head, current.label])
    if path_hint:
        bits.append(str(path_hint))
    return "\n".join(bit for bit in bits if bit)


def parse_args(argv: Iterable[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Heuristic Kino scout for MALP recommendation.")
    parser.add_argument("--question", default="", help="Concrete question Kino is trying to answer.")
    parser.add_argument("--current-malp", help="Current malp path or its parent path.")
    parser.add_argument("--path", help="Additional path hint related to the current worksite.")
    parser.add_argument("--active-map", default="~/.malp-home/MAP.txt", help="Path to active MAP.txt")
    parser.add_argument("--attic-map", default="~/.malp-home/attic/MAP.txt", help="Path to attic MAP.txt")
    parser.add_argument("--include-attic", action="store_true", help="Allow attic entries to be considered.")
    parser.add_argument("--scan-near-path", action="store_true", help="Scan near --path for unindexed .malp directories.")
    parser.add_argument("--git-aux", action="store_true", help="Allow a shallow git-history auxiliary finding when helpful.")
    parser.add_argument("--git-freshness", action="store_true", help="Report territory-scoped git freshness for the recommended malp.")
    parser.add_argument("--containment", action="store_true", help="Estimate whether the main query term stays within a bounded malp tag cluster.")
    parser.add_argument("--git-max-candidates", type=int, default=2, help="How many top candidate repos to probe for shallow git history.")
    parser.add_argument("--git-max-commits", type=int, default=6, help="How many early git matches to inspect per search term.")
    parser.add_argument("--top", type=int, default=5, help="How many ranked candidates to include in JSON output.")
    parser.add_argument("--json", action="store_true", help="Emit JSON.")
    return parser.parse_args(list(argv))


def main(argv: Iterable[str]) -> int:
    args = parse_args(argv)
    active_map = Path(os.path.expanduser(args.active_map))
    attic_map = Path(os.path.expanduser(args.attic_map))
    current_path = Path(os.path.expanduser(args.current_malp)) if args.current_malp else None
    path_hint = Path(os.path.expanduser(args.path)) if args.path else None

    candidates = build_candidates(active_map, attic_map, current_path, path_hint, include_attic=args.include_attic)
    if args.scan_near_path:
        for cand in gather_unindexed_near(path_hint or current_path, candidates):
            candidates.setdefault(str(cand.path), cand)

    current_candidate = None
    if current_path:
        current_candidate = candidates.get(str(candidate_from_path(current_path).path))
    anchor_text = infer_anchor_text(current_candidate, path_hint)
    question_tokens = tokenize(args.question)
    anchor_tokens = tokenize(anchor_text)

    term_df: dict[str, int] = {}
    for cand in candidates.values():
        telemetry_text = full_malp_text(cand)
        territory_text = "\n".join([cand.label, cand.territory_head])
        all_tokens = tokenize(telemetry_text) | tokenize(territory_text)
        for term in question_tokens & all_tokens:
            term_df[term] = term_df.get(term, 0) + 1

    for cand in candidates.values():
        score_candidate(cand, question_tokens, anchor_tokens, current_path, term_df=term_df)

    ranked = sorted(candidates.values(), key=lambda c: (-c.score, c.label))
    recommendation = make_recommendation(ranked, current_path)
    subject_terms = infer_subject_terms(question_tokens)
    provenance_query = question_requests_provenance(args.question)
    direct_provenance_terms = infer_git_terms(subject_terms)
    direct_provenance = has_direct_provenance_signal(ranked[: max(1, args.top)], direct_provenance_terms) if provenance_query else None
    git_finding = None
    if args.git_aux and subject_terms:
        git_finding = gather_git_auxiliary(ranked, subject_terms, max_candidates=max(1, args.git_max_candidates), max_commits=max(1, args.git_max_commits))
    recommended_freshness = compute_git_freshness(ranked[0]) if args.git_freshness and ranked else None
    containment = compute_containment(ranked, subject_terms) if args.containment else None

    payload = {
        "question": args.question,
        "current_malp": str(candidate_from_path(current_path).path) if current_path else None,
        "path_hint": str(path_hint) if path_hint else None,
        "recommendation": recommendation,
        "direct_answer": {
            "kind": "malp-provenance",
            "status": "present" if direct_provenance else "none-observed",
        } if provenance_query else None,
        "auxiliary": {
            "kind": "git-history",
            "status": "supporting-evidence",
            "repo": str(git_finding.repo),
            "matched_term": git_finding.matched_term,
            "date": git_finding.date,
            "author": git_finding.author,
            "commit": git_finding.commit,
            "subject": git_finding.subject,
        } if git_finding else None,
        "git_freshness": {
            "status": recommended_freshness.status,
            "repo": recommended_freshness.repo,
            "territory": recommended_freshness.territory,
            "last_malp_update": recommended_freshness.last_malp_update,
            "last_territory_commit": recommended_freshness.last_territory_commit,
            "commits_since_malp": recommended_freshness.commits_since_malp,
            "dirty": recommended_freshness.dirty,
        } if recommended_freshness else None,
        "containment": {
            "status": containment.status,
            "term": containment.term,
            "cluster_tags": containment.cluster_tags,
            "supporting_malps": containment.supporting_malps,
            "outside_hits": containment.outside_hits,
        } if containment else None,
        "ranked": [
            {
                "malp": str(c.path),
                "state": c.state,
                "source": c.source,
                "score": round(c.score, 2),
                "reasons": c.reasons[:5],
                "root": str(c.root),
                "promotion": "reference" if sum(1 for r in c.reasons if r.startswith("territory ")) > sum(1 for r in c.reasons if r.startswith("telemetry ")) else "working",
            }
            for c in ranked[: max(1, args.top)]
            if c.score > -2.0
        ],
        "inspected_count": len(candidates),
    }

    if args.json:
        json.dump(payload, sys.stdout, indent=2)
        sys.stdout.write("\n")
        return 0

    rec = recommendation
    print(f"Question: {args.question or '(none)'}")
    print(f"Action: {rec['action']}")
    print(f"Confidence: {rec['confidence']}")
    print(f"Promotion: {rec.get('promotion', 'none')}")
    if rec.get("recommended_malp"):
        print(f"Recommended malp: {rec['recommended_malp']}")
    if rec.get("recommended_path"):
        print(f"Recommended path: {rec['recommended_path']}")
    if rec.get("reasons"):
        print("Reasons:")
        for reason in rec["reasons"]:
            print(f"- {reason}")
    if payload.get("direct_answer"):
        print(f"Direct malp answer: {payload['direct_answer']['status']}")
    if payload.get("auxiliary"):
        aux = payload["auxiliary"]
        print("Auxiliary git finding:")
        print(f"- {aux['date']} | {aux['author']} | {aux['commit']} | {aux['subject']}")
        print(f"- repo: {aux['repo']} (matched term: {aux['matched_term']})")
    if payload.get("git_freshness"):
        freshness = payload["git_freshness"]
        print("Git freshness:")
        print(f"- status: {freshness['status']}")
        print(f"- commits_since_malp: {freshness['commits_since_malp']}")
        print(f"- dirty: {freshness['dirty']}")
    if payload.get("containment"):
        containment = payload["containment"]
        print("Containment:")
        print(f"- status: {containment['status']}")
        print(f"- term: {containment['term']}")
        if containment['cluster_tags']:
            print(f"- cluster_tags: {', '.join(containment['cluster_tags'])}")
    if payload["ranked"]:
        print("Top candidates:")
        for item in payload["ranked"][:3]:
            print(f"- {item['malp']} [{item['state']}] score={item['score']}")
    print(f"Inspected: {payload['inspected_count']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
