from __future__ import annotations

import re
from urllib.parse import parse_qs, unquote_plus, urlparse

from flask import Blueprint, jsonify, request

from config import DEFAULT_USER, PARTICIPANTS, canonical_user, normalize_user_key, participant_aliases
from memory_store import MemoryStore
from openclaw_client import call_openclaw


chat_bp = Blueprint("chat", __name__)
memory = MemoryStore()
ALIASES = participant_aliases()
DISPLAY_NAMES = [item["display_name"] for item in PARTICIPANTS]

KNOWN_PLACES = {
    "home": "__HOME__",
    "house": "__HOME__",
    "domicile": "__HOME__",
    "maison": "__HOME__",
    "work": "__WORK__",
    "office": "__WORK__",
    "job": "__WORK__",
    "travail": "__WORK__",
    "parking du flon": "Parking du Flon, Lausanne",
    "flon": "Parking du Flon, Lausanne",
}

FIELD_LABELS = {
    "aquarium": "aquarium",
    "work": "work",
    "home": "home",
    "address": "address",
    "likes": "likes",
    "lessons": "lessons",
    "instrument": "instrument",
    "activity": "activity",
}


def normalize_history(raw_history):
    if not isinstance(raw_history, list):
        return []
    cleaned = []
    for item in raw_history:
        if not isinstance(item, dict):
            continue
        role = item.get("role")
        content = str(item.get("content") or "").strip()
        if role in {"system", "user", "assistant"} and content:
            cleaned.append({"role": role, "content": content})
    return cleaned



def detect_user_from_message(message: str):
    if not message:
        return None, ""
    msg = message.strip()
    lower = msg.lower()
    for alias, display_name in ALIASES.items():
        if lower.startswith(alias + ":") or lower.startswith(alias + ","):
            return display_name, msg[len(alias) + 1 :].strip()
    return None, msg



def _normalize_subject_name(subject: str, active_user: str) -> str:
    s = str(subject or "").strip()
    if not s:
        return active_user
    lowered = s.lower()

    pronouns = {
        "i": active_user,
        "me": active_user,
        "my": active_user,
        "je": active_user,
        "moi": active_user,
        "mon": active_user,
        "ma": active_user,
        "mes": active_user,
        "papa": "father",
        "dad": "father",
        "maman": "mother",
        "mom": "mother",
        "mum": "mother",
        "mother": "mother",
        "father": "father",
    }

    if lowered in pronouns:
        token = pronouns[lowered]
        if token == "father":
            for display_name in DISPLAY_NAMES:
                if display_name != active_user:
                    return display_name
        if token == "mother":
            for display_name in DISPLAY_NAMES:
                if display_name != active_user:
                    return display_name
        return token

    return ALIASES.get(lowered, s)



def should_auto_memorize(message: str) -> bool:
    msg = str(message or "").strip()
    lower = msg.lower()
    if len(msg) < 8 or len(msg) > 180 or "?" in msg:
        return False
    blocked_starts = [
        "hello",
        "hi",
        "thanks",
        "thank you",
        "ok",
        "okay",
        "bonjour",
        "salut",
        "merci",
        "can you",
        "could you",
        "peux-tu",
        "tu peux",
        "what",
        "when",
        "where",
        "why",
        "how",
        "quel",
        "quelle",
        "quand",
        "où",
        "ou ",
        "pourquoi",
        "comment",
    ]
    if any(lower.startswith(x) for x in blocked_starts):
        return False

    durable_patterns = [
        r"\bi like\b",
        r"\bi play\b",
        r"\bi work\b",
        r"\blives? at\b",
        r"\baddress\b",
        r"\bhome\b",
        r"\bdomicile\b",
        r"\btravaille\b",
        r"\bhabite\b",
        r"\baime\b",
        r"\bpratique\b",
        r"\baquarium\b",
    ]
    return any(re.search(pattern, lower) for pattern in durable_patterns)



def canonicalize_fact(message: str, user: str) -> str | None:
    msg = " ".join(str(message or "").strip().split())
    lower = msg.lower()

    if lower.startswith("i "):
        return f"{user} {msg[2:]}".strip()
    if lower.startswith("je "):
        return f"{user} {msg[3:]}".strip()
    if lower.startswith(("he ", "she ", "il ", "elle ")):
        return None

    for alias, display_name in ALIASES.items():
        if lower.startswith(alias + " "):
            return display_name + msg[len(alias) :]

    return msg if should_auto_memorize(msg) else None



def extract_structured_fact(text: str, active_user: str):
    msg = " ".join(str(text or "").strip().split())
    patterns = [
        (r"^(.+?)\s+has\s+an?\s+aquarium(?:\s+of\s+(freshwater|saltwater))?$", lambda m: (_normalize_subject_name(m.group(1), active_user), "aquarium", (m.group(2) or "yes").strip())),
        (r"^(.+?)\s+a\s+un[e]?\s+aquarium(?:\s+d['’]?(eau douce|eau de mer))?$", lambda m: (_normalize_subject_name(m.group(1), active_user), "aquarium", (m.group(2) or "yes").strip())),
        (r"^(.+?)\s+works?\s+at\s+(.+?)$", lambda m: (_normalize_subject_name(m.group(1), active_user), "work", m.group(2).strip())),
        (r"^(.+?)\s+travaille\s+chez\s+(.+?)$", lambda m: (_normalize_subject_name(m.group(1), active_user), "work", m.group(2).strip())),
        (r"^(.+?)\s+lives?\s+at\s+(.+?)$", lambda m: (_normalize_subject_name(m.group(1), active_user), "home", m.group(2).strip())),
        (r"^(.+?)\s+habite\s+(?:à|au)\s+(.+?)$", lambda m: (_normalize_subject_name(m.group(1), active_user), "home", m.group(2).strip())),
        (r"^(.+?)\s+address\s*:\s*(.+?)$", lambda m: (_normalize_subject_name(m.group(1), active_user), "address", m.group(2).strip())),
        (r"^(.+?)\s+adresse\s*:\s*(.+?)$", lambda m: (_normalize_subject_name(m.group(1), active_user), "address", m.group(2).strip())),
        (r"^(.+?)\s+likes\s+(.+?)$", lambda m: (_normalize_subject_name(m.group(1), active_user), "likes", m.group(2).strip())),
        (r"^(.+?)\s+aime\s+(.+?)$", lambda m: (_normalize_subject_name(m.group(1), active_user), "likes", m.group(2).strip())),
        (r"^(.+?)\s+takes?\s+lessons?\s+in\s+(.+?)$", lambda m: (_normalize_subject_name(m.group(1), active_user), "lessons", m.group(2).strip())),
        (r"^(.+?)\s+prend\s+des\s+cours\s+de\s+(.+?)$", lambda m: (_normalize_subject_name(m.group(1), active_user), "lessons", m.group(2).strip())),
        (r"^(.+?)\s+plays?\s+the\s+(.+?)$", lambda m: (_normalize_subject_name(m.group(1), active_user), "instrument", m.group(2).strip())),
        (r"^(.+?)\s+joue\s+du\s+(.+?)$", lambda m: (_normalize_subject_name(m.group(1), active_user), "instrument", m.group(2).strip())),
        (r"^(.+?)\s+does\s+(.+?)$", lambda m: (_normalize_subject_name(m.group(1), active_user), "activity", m.group(2).strip())),
        (r"^(.+?)\s+(?:fait\s+de|pratique)\s+(.+?)$", lambda m: (_normalize_subject_name(m.group(1), active_user), "activity", m.group(2).strip())),
    ]

    for pattern, builder in patterns:
        match = re.match(pattern, msg, flags=re.IGNORECASE)
        if match:
            subject, field, value = builder(match)
            return {"subject": subject, "field": field, "value": value}
    return None



def build_memory_context(message: str, user: str) -> str:
    memory_user = normalize_user_key(user)
    parts = []
    user_context = memory.build_context_for_user(memory_user)
    if user_context:
        parts.append(user_context)
    memories = memory.search(query=message, limit=5)
    if memories:
        lines = [f"- {hit.subject} | {hit.field}: {hit.value}" for hit in memories]
        parts.append("Relevant persistent memory for this conversation:\n" + "\n".join(lines))
    return "\n\n".join(parts).strip()



def build_last_subject_from_history(history, user):
    user_messages = [str(item.get("content") or "").strip() for item in history if item.get("role") == "user" and str(item.get("content") or "").strip()]
    for text in reversed(user_messages):
        fact = extract_structured_fact(text, user)
        if fact:
            return fact["subject"]
        match = re.match(r"^(?:what\s+do\s+you\s+know\s+about|que\s+sais-tu\s+de|est-ce\s+que)\s+(.+?)\??$", text, flags=re.IGNORECASE)
        if match:
            return _normalize_subject_name(match.group(1), user)
    return None



def format_subject_summary(subject: str) -> str:
    summary = memory.get_subject_summary(subject)
    if not summary.get("found"):
        return f"I do not have persistent information about {subject} yet."
    facts = summary.get("facts", {})
    if not facts:
        return f"I do not have detailed information about {subject} yet."
    lines = [f"Here is what I know about {summary['subject']}: "]
    for key, value in facts.items():
        lines.append(f"- {FIELD_LABELS.get(key, key)}: {value}")
    return "\n".join(lines)



def format_field_answer(subject: str, field: str) -> str:
    summary = memory.get_subject_summary(subject)
    if not summary.get("found"):
        return f"I do not have that information for {subject}."
    facts = summary.get("facts", {})
    if field not in facts:
        return f"I do not have that information for {subject}."
    value = facts[field]
    if field == "aquarium":
        if value in {"yes", "oui"}:
            return f"Yes, {subject} has an aquarium."
        return f"Yes, {subject} has an aquarium, more specifically: {value}."
    return f"For {subject}, {FIELD_LABELS.get(field, field)}: {value}."



def is_route_request(message: str) -> bool:
    lower = str(message or "").lower()
    keywords = [
        "route",
        "directions",
        "trip",
        "travel time",
        "how long",
        "trajet",
        "itinéraire",
        "itineraire",
        "temps de trajet",
        "combien de temps",
    ]
    return any(keyword in lower for keyword in keywords)



def route_system_instruction(user: str) -> str:
    return f"""
You are helping open a Google Maps route inside the web gateway.
Do not call tools.
Do not say that a tool is missing.
If you can infer an origin and destination from the user message, persistent memory, or the current user ({user}), start your answer with exactly:
ROUTE: <origin> || <destination>
Then add a short human reply.
If you cannot resolve both places, reply normally without a ROUTE line.
""".strip()



def extract_route_from_reply(text: str):
    raw = str(text or "").strip()
    if not raw:
        return None
    route_line = re.search(r"^\s*ROUTE:\s*(.+?)\s*\|\|\s*(.+?)\s*$", raw, flags=re.IGNORECASE | re.MULTILINE)
    if route_line:
        origin = route_line.group(1).strip()
        destination = route_line.group(2).strip()
        if origin and destination:
            return origin, destination
    url_match = re.search(r"https?://www\.google\.com/maps/dir/\?api=1[^\s]+", raw, flags=re.IGNORECASE)
    if url_match:
        parsed = urlparse(url_match.group(0))
        qs = parse_qs(parsed.query)
        origin = unquote_plus((qs.get("origin") or [""])[0]).strip()
        destination = unquote_plus((qs.get("destination") or [""])[0]).strip()
        if origin and destination:
            return origin, destination
    return None



def clean_reply_text(text: str) -> str:
    cleaned = str(text or "").strip()
    cleaned = re.sub(r"^\s*ROUTE:\s*.+?\s*\|\|\s*.+?\s*$", "", cleaned, flags=re.IGNORECASE | re.MULTILINE)
    cleaned = re.sub(r"https?://www\.google\.com/maps/dir/\?api=1[^\s]+", "", cleaned, flags=re.IGNORECASE)
    cleaned = re.sub(r"\n{3,}", "\n\n", cleaned).strip()
    return cleaned



def _get_fact_value(subject: str, field: str) -> str:
    summary = memory.get_subject_summary(subject)
    if not summary.get("found"):
        return ""
    return str(summary.get("facts", {}).get(field) or "").strip()



def resolve_special_place(token: str, user: str) -> str:
    token = str(token or "").strip()
    if not token:
        return ""
    lowered = token.lower()
    mapped = KNOWN_PLACES.get(lowered)
    if mapped == "__HOME__":
        return _get_fact_value(user, "home") or _get_fact_value(user, "address")
    if mapped == "__WORK__":
        return _get_fact_value(user, "work")
    if mapped:
        return mapped
    return token



def extract_route_from_message(message: str, user: str):
    msg = " ".join(str(message or "").strip().split())
    lower = msg.lower()

    match = re.search(r"\bfrom\s+(.+?)\s+to\s+(.+)$", msg, flags=re.IGNORECASE)
    if match:
        origin = resolve_special_place(match.group(1), user)
        destination = resolve_special_place(match.group(2), user)
        if origin and destination:
            return origin, destination

    match = re.search(r"\bde\s+(.+?)\s+à\s+(.+)$", msg, flags=re.IGNORECASE)
    if match:
        origin = resolve_special_place(match.group(1), user)
        destination = resolve_special_place(match.group(2), user)
        if origin and destination:
            return origin, destination

    match = re.search(r"\b(?:go|going|route|directions|trip|trajet|itinéraire|itineraire).*(?:to|au|à|a)\s+(.+)$", msg, flags=re.IGNORECASE)
    if match:
        destination = resolve_special_place(match.group(1), user)
        origin = resolve_special_place("home", user)
        if origin and destination:
            return origin, destination

    match = re.search(r"\b(?:travel time|how long|temps de trajet|combien de temps).*(?:to|vers|pour aller à|pour aller au|jusqu['’]a|jusqu['’]à)\s+(.+)$", lower, flags=re.IGNORECASE)
    if match:
        destination = resolve_special_place(match.group(1), user)
        origin = resolve_special_place("home", user)
        if origin and destination:
            return origin, destination

    for key, mapped in KNOWN_PLACES.items():
        if key in lower and mapped not in {"__HOME__", "__WORK__"}:
            destination = resolve_special_place(key, user)
            origin = resolve_special_place("home", user)
            if origin and destination:
                return origin, destination

    return None


@chat_bp.route("/api/chat", methods=["POST"])
def api_chat():
    data = request.get_json(silent=True) or {}
    user = canonical_user(data.get("user", DEFAULT_USER))
    history = normalize_history(data.get("history", []))
    message = str(data.get("message") or "").strip()

    detected_user, cleaned_message = detect_user_from_message(message)
    if detected_user:
        user = detected_user
        message = cleaned_message

    if not message:
        return jsonify({"error": "Empty message"}), 400

    try:
        lower = message.lower().strip()
        memory_user = normalize_user_key(user)

        memory_prefixes = [
            "remember that ",
            "note that ",
            "memorise que ",
            "mémorise que ",
            "souviens-toi que ",
            "souviens toi que ",
        ]

        memory_text = None
        for prefix in memory_prefixes:
            if lower.startswith(prefix):
                memory_text = message[len(prefix) :].strip()
                break

        if memory_text:
            fact = extract_structured_fact(memory_text, user)
            if fact:
                already_exists = memory.fact_exists(fact["subject"], fact["field"], fact["value"])
                if not already_exists:
                    memory.remember_fact(fact["subject"], fact["field"], fact["value"], source_user=memory_user)
                    return jsonify({"reply": f"Saved for {fact['subject']}: {fact['field']} = {fact['value']}.", "user": user})
                return jsonify({"reply": "That information is already present in persistent memory.", "user": user})

            fallback_fact = canonicalize_fact(memory_text, user) or memory_text
            memory.append_note(memory_user, fallback_fact)
            return jsonify({"reply": "The information was added to persistent memory.", "user": user})

        summary_match = re.match(r"^(?:what\s+do\s+you\s+know\s+about|que\s+sais-tu\s+de|qu'est-ce\s+que\s+tu\s+sais\s+de)\s+(.+?)\s*\??$", message, flags=re.IGNORECASE)
        if summary_match:
            subject = _normalize_subject_name(summary_match.group(1), user)
            return jsonify({"reply": format_subject_summary(subject), "user": user})

        aquarium_check = re.match(r"^(?:does|est-ce\s+que|es[- ]tu\s+s[ûu]r\s+que)\s+(.+?)\s+(?:have|a)\s+an?\s+aquarium\s*\??$", message, flags=re.IGNORECASE)
        if aquarium_check:
            subject = _normalize_subject_name(aquarium_check.group(1), user)
            return jsonify({"reply": format_field_answer(subject, "aquarium"), "user": user})

        if re.match(r"^(?:what\s+kind|which\s+kind|quel\s+genre|quel\s+type)\s*\??$", message, flags=re.IGNORECASE) or re.match(r"^(?:freshwater\s+or\s+saltwater|eau\s+douce\s+ou\s+eau\s+de\s+mer)\s*\??$", message, flags=re.IGNORECASE):
            last_subject = build_last_subject_from_history(history, user)
            if last_subject:
                return jsonify({"reply": format_field_answer(last_subject, "aquarium"), "user": user})

        auto_fact_text = canonicalize_fact(message, user)
        if auto_fact_text and should_auto_memorize(message):
            structured = extract_structured_fact(auto_fact_text, user)
            if structured:
                if not memory.fact_exists(structured["subject"], structured["field"], structured["value"]):
                    memory.remember_fact(structured["subject"], structured["field"], structured["value"], source_user=memory_user)
            else:
                memory.append_note(memory_user, auto_fact_text)

        if is_route_request(message):
            direct_route = extract_route_from_message(message, user)
            if direct_route:
                origin, destination = direct_route
                return jsonify({"reply": "Here is the route.", "user": user, "action": {"type": "open_route", "origin": origin, "destination": destination}})

        memory_context = build_memory_context(message=message, user=user)
        augmented_history = list(history)
        if is_route_request(message):
            augmented_history.insert(0, {"role": "system", "content": route_system_instruction(user)})
        if memory_context:
            augmented_history.insert(0, {"role": "system", "content": memory_context})

        reply = call_openclaw(user=user, message=message, history=augmented_history)
        route = extract_route_from_reply(reply)
        cleaned_reply = clean_reply_text(reply)

        if route:
            origin, destination = route
            return jsonify({"reply": cleaned_reply or "Here is the route.", "user": user, "action": {"type": "open_route", "origin": origin, "destination": destination}})

        return jsonify({"reply": cleaned_reply or reply, "user": user})
    except Exception as exc:
        return jsonify({"error": str(exc)}), 500
