"""Small, deterministic rules shared by multi-parcel workflow steps."""

from utils import boundaries_equal, validate_country_code, validate_identifier


def annotate_parcels(parcels):
    """Attach stable input identities and validate batch-level metadata."""
    annotated = []
    seen_refs = set()
    countries = {}

    for index, source in enumerate(parcels):
        if not isinstance(source, dict):
            raise ValueError(f"Parcel {index + 1}: expected an object")
        parcel = dict(source)
        parcel_ref = validate_identifier(
            parcel.get("parcel_ref") or f"P{index + 1:02d}",
            "parcel_ref",
        )
        if parcel_ref in seen_refs:
            raise ValueError(f"Duplicate parcel_ref: {parcel_ref}")
        seen_refs.add(parcel_ref)

        parcel["input_index"] = index
        parcel["parcel_ref"] = parcel_ref
        if parcel.get("country_code"):
            country = validate_country_code(parcel["country_code"])
            parcel["country_code"] = country
            countries.setdefault(country, []).append(parcel_ref)
        annotated.append(parcel)

    return annotated, countries


def resolution_for(mapping, parcel):
    """Read a per-parcel decision by stable parcel reference."""
    if not isinstance(mapping, dict):
        return False, None
    key = parcel["parcel_ref"]
    return (True, mapping[key]) if key in mapping else (False, None)


def find_prior_boundary_match(parcel, prior_parcels):
    for prior in prior_parcels:
        if boundaries_equal(parcel.get("vertices", []), prior.get("vertices", [])):
            return prior
    return None


def duplicate_official_ids(parcels):
    seen = {}
    conflicts = []
    for parcel in parcels:
        official_id = str(parcel.get("official_id") or "").strip()
        if not official_id:
            continue
        if official_id in seen:
            conflicts.append(
                {
                    "official_id": official_id,
                    "first_ref": seen[official_id],
                    "parcel_ref": parcel["parcel_ref"],
                }
            )
        else:
            seen[official_id] = parcel["parcel_ref"]
    return conflicts
