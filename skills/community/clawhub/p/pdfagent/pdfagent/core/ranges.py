from __future__ import annotations


def parse_page_ranges(spec: str | None, total_pages: int) -> list[int]:
    if spec is None or spec.strip() == "":
        return list(range(total_pages))

    spec = spec.strip().lower()
    if spec in {"all", "*"}:
        return list(range(total_pages))
    if spec == "odd":
        return [i for i in range(total_pages) if (i + 1) % 2 == 1]
    if spec == "even":
        return [i for i in range(total_pages) if (i + 1) % 2 == 0]

    indices: set[int] = set()
    for part in spec.split(","):
        part = part.strip()
        if not part:
            continue
        if "-" in part:
            start_s, end_s = part.split("-", 1)
            start = int(start_s)
            end = int(end_s)
        else:
            start = end = int(part)
        if start < 1 or end < 1 or start > total_pages or end > total_pages:
            raise ValueError(f"Page range out of bounds: {start}-{end} of {total_pages}")
        if end < start:
            raise ValueError(f"Invalid page range: {start}-{end}")
        for i in range(start - 1, end):
            indices.add(i)
    if not indices:
        raise ValueError("No valid ranges provided")
    return sorted(indices)
