"""CLI comma-separated work tags; independent of the server package."""

import unicodedata


def exact(value):
    tags = parse(value)
    if len(tags) != 1 or "," in value or "，" in value:
        raise ValueError("Filter by one tag at a time")
    return tags[0]


def parse(value):
    if len(value) > 2048:
        raise ValueError("Tag input is too long")
    values = value.replace("，", ",").split(",")
    if len(values) > 10:
        raise ValueError("Use at most 10 tags")
    result = []
    for value in values:
        value = unicodedata.normalize("NFKC", value).strip().lower()
        if not 1 <= len(value) <= 20 or any(
            c != " " and unicodedata.category(c)[0] not in "LMN" for c in value
        ):
            raise ValueError(
                "Use 1–20 letters, numbers or spaces per tag; punctuation and empty tags are not allowed"
            )
        if value not in result:
            result.append(value)
    return result
