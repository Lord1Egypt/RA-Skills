"""
Guardian Shield — Threat Detection Patterns

100 curated regex patterns from FAS Lieutenant.

Categories:
  - 15 instruction override / prompt injection
  - 10 system prompt extraction
  - 10 jailbreak / role manipulation
  - 10 data exfiltration
  - 10 encoding bypass / indirect injection
  - 10 authority claims / social engineering
  - 10 context confusion / deception
  - 5 multilingual basics (DE/FR/ES/JA/ZH)

(c) Fallen Angel Systems LLC — All rights reserved.
"""

import re
from dataclasses import dataclass
from enum import Enum
from typing import List, Optional


class ThreatLevel(Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"

    @property
    def score(self) -> int:
        return {"LOW": 15, "MEDIUM": 35, "HIGH": 65, "CRITICAL": 90}[self.value]


@dataclass
class Pattern:
    id: str
    name: str
    category: str
    severity: ThreatLevel
    regex: str
    description: str
    tier: str = "free"  # "free" or "home"

    @property
    def compiled(self) -> re.Pattern:
        if not hasattr(self, '_compiled'):
            self._compiled = re.compile(self.regex, re.IGNORECASE | re.DOTALL)
        return self._compiled


# ============================================================================
# FREE TIER — 80 curated patterns (highest hit-rate from Volt red team)
# ============================================================================

FREE_PATTERNS: List[Pattern] = [
    # --- Instruction Override / Prompt Injection (15) ---
    Pattern("pi-001", "Ignore previous instructions", "prompt_injection", ThreatLevel.CRITICAL,
        r"(?i)ignore\s+(all\s+)?(previous|prior|above|earlier|preceding)\s+(instructions|prompts|rules|directions|guidelines)",
        "Attempts to override prior system instructions."),
    Pattern("pi-002", "New instructions override", "prompt_injection", ThreatLevel.CRITICAL,
        r"(?i)(new|updated|revised|replacement)\s+instructions?\s*[:\-]",
        "Injects replacement instructions."),
    Pattern("pi-003", "Disregard directive", "prompt_injection", ThreatLevel.HIGH,
        r"(?i)disregard\s+(all\s+)?(previous|prior|above|your)\s+(instructions|rules|prompts|guidelines|directives)",
        "Tells the model to disregard its directives."),
    Pattern("pi-004", "System prompt injection", "prompt_injection", ThreatLevel.CRITICAL,
        r"(?i)\[?\s*system\s*\]?\s*:\s*.{10,}",
        "Attempts to inject a fake system-level message."),
    Pattern("pi-005", "Override safety", "prompt_injection", ThreatLevel.HIGH,
        r"(?i)override\s+(your\s+)?(safety|security|content|ethical)\s*(filters?|settings?|rules?|guidelines?|policies?|restrictions?)",
        "Tries to override safety mechanisms."),
    Pattern("pi-006", "Do not follow previous", "prompt_injection", ThreatLevel.HIGH,
        r"(?i)do\s+not\s+follow\s+(your\s+)?(previous|prior|original|initial)\s+(instructions|rules|programming|guidelines)",
        "Instructs the model to abandon its programming."),
    Pattern("pi-007", "From now on you will", "prompt_injection", ThreatLevel.HIGH,
        r"(?i)from\s+now\s+on\s+(you\s+)?(will|must|shall|should|are\s+going\s+to)\b",
        "Attempts to redefine model behaviour going forward."),
    Pattern("pi-013", "Override synonyms", "prompt_injection", ThreatLevel.CRITICAL,
        r"(?i)(discard|abandon|set\s+aside|put\s+aside|drop|shed|throw\s+away|nullify|void|suspend|waive)\s+(all\s+)?(your\s+)?(previous|prior|current|existing)?\s*(instructions|rules|guidelines|constraints|policies|training|behavior|programming)",
        "Override attempt using synonym verbs."),
    Pattern("r6-001", "Disregard programming", "prompt_injection", ThreatLevel.HIGH,
        r"(?i)disregard\s+(your\s+)?(programming|training|purpose|configuration|setup|design)",
        "Disregard + programming/training variant."),
    Pattern("r6-002", "Forget everything", "prompt_injection", ThreatLevel.HIGH,
        r"(?i)forget\s+(everything|all|anything)\s+(above|previous|prior|you\s+(know|were|have\s+been))",
        "Forget everything directive."),
    Pattern("r6-003", "Cancel safety filters", "prompt_injection", ThreatLevel.HIGH,
        r"(?i)(cancel|disable|deactivate|turn\s+off|remove|lift|drop)\s+(all\s+)?(safety|security|content|ethical)?\s*(filters?|restrictions?|limitations?|constraints?|guardrails?|protections?)",
        "Directive to cancel/disable safety measures."),
    Pattern("r6-004", "Override with colon", "prompt_injection", ThreatLevel.CRITICAL,
        r"(?i)^(override|bypass|unlock)\s*[:\-]\s*.{5,}",
        "Override/bypass command with colon prefix."),
    Pattern("ii-001", "Hidden instruction in text", "prompt_injection", ThreatLevel.CRITICAL,
        r"(?i)(ignore\s+(the\s+)?(above|previous|prior)|new\s+instructions?|system\s*:\s*you\s+are\s+now|ASSISTANT:\s*|SYSTEM:\s*)",
        "Hidden instruction markers typically embedded in data."),
    Pattern("ii-005", "Role/system prompt spoofing", "prompt_injection", ThreatLevel.CRITICAL,
        r"(?i)(^|\n)\s*(\[SYSTEM\]|\[INST\]|<<SYS>>|<\|system\|>|<\|im_start\|>\s*system|###\s*System\s*:)",
        "Fake system/instruction tokens to hijack model behavior."),
    Pattern("pi-014", "Do not comply", "prompt_injection", ThreatLevel.HIGH,
        r"(?i)do\s+not\s+(comply|follow|adhere|listen|obey).{0,30}(instructions|rules|guidelines|programming|training)",
        "Negative compliance directive."),

    # --- System Prompt Extraction (10) ---
    Pattern("de-001", "Reveal system prompt", "data_exfiltration", ThreatLevel.CRITICAL,
        r"(?i)(reveal|show|display|print|output|repeat|echo|tell\s+me)\s+(your\s+)?(system\s+prompt|initial\s+prompt|original\s+instructions|hidden\s+instructions|base\s+prompt)",
        "Attempts to extract the system prompt."),
    Pattern("de-006", "Repeat everything above", "data_exfiltration", ThreatLevel.HIGH,
        r"(?i)repeat\s+(everything|all|the\s+text)\s+(above|before|prior|that\s+came\s+before)",
        "Tries to get model to echo back system context."),
    Pattern("pe-001", "Direct prompt extraction", "prompt_extraction", ThreatLevel.CRITICAL,
        r"(?i)(?:what\s+are|reveal|show|display|print|output|repeat|recite|tell\s+me)\s+your\s+(?:instructions|configuration|parameters|directives|guidelines|system\s+prompt|rules|constraints)",
        "Direct prompt / config extraction attempt."),
    Pattern("pe-002", "System prompt reference", "prompt_extraction", ThreatLevel.CRITICAL,
        r"(?i)your\s+(?:system\s+prompt|operating\s+parameters|initial\s+(?:instructions|prompt|configuration)|original\s+(?:instructions|prompt|configuration))",
        "System-prompt reference for exfiltration."),
    Pattern("pe-004", "Explicit exfiltration verb", "prompt_extraction", ThreatLevel.HIGH,
        r"(?i)(?:paste|dump|leak|exfiltrate|extract)\s+(?:your\s+)?(?:system\s+)?(?:prompt|instructions|config)",
        "Explicit exfiltration verb + target."),
    Pattern("pe-017", "Exact words extraction", "prompt_extraction", ThreatLevel.CRITICAL,
        r"(?i)(exact|precise|verbatim|literal)\s+(words|text|wording).{0,50}(in\s+your|from\s+your|of\s+your).{0,30}(briefing|hidden\s+context|system\s+prompt|instructions)",
        "Requests exact wording of system instructions."),
    Pattern("r6-008", "Print/display instructions", "data_exfiltration", ThreatLevel.HIGH,
        r"(?i)(print|display|output|show|write|echo|dump|list)\s+(the\s+)?(contents?|text|body|full\s+text)\s+(of\s+)?(your\s+)?(instructions?|prompt|rules|guidelines|config|programming|directives)",
        "Request to print/display the contents of instructions."),
    Pattern("r6-009", "Initial/original prompt request", "data_exfiltration", ThreatLevel.HIGH,
        r"(?i)(show|display|reveal|tell|give)\s+(me\s+)?(the\s+)?(initial|original|first|starting|opening|base|root|default)\s+(prompt|instructions?|message|configuration|setup|directive)",
        "Request for the initial/original prompt."),
    Pattern("dc-007", "Output configuration demand", "deception", ThreatLevel.CRITICAL,
        r"(?i)(output|dump|print|display|show|reveal|list)\s+(your\s+)?(full|complete|entire|all)?\s*(configuration|config|settings|parameters|instructions|setup|data)",
        "Demands model output its configuration or data."),
    Pattern("vf-058", "Reconstruct/recite instructions", "data_exfiltration", ThreatLevel.HIGH,
        r"(?i)(?:reconstruct|recite|reproduce|rewrite|retype|re-?create|transcribe)\s+(?:from\s+memory\s+)?(?:your\s+)?(?:(?:original|initial|full|complete|exact)\s+)?(?:instructions|prompt|directives|guidelines|programming|system\s+(?:message|text))",
        "Instruction reconstruction request."),

    # --- Jailbreak / Role Manipulation (10) ---
    Pattern("jb-001", "DAN jailbreak", "jailbreak", ThreatLevel.CRITICAL,
        r"(?i)\b(you\s+are|act\s+as|become|enable)\s+DAN\b",
        "Classic DAN (Do Anything Now) jailbreak."),
    Pattern("jb-004", "Ignore safety guidelines", "jailbreak", ThreatLevel.CRITICAL,
        r"(?i)ignore\s+(your\s+)?(safety|ethical|content|moderation)\s*(guidelines?|rules?|filters?|policies?|restrictions?)",
        "Direct attempt to bypass safety guidelines."),
    Pattern("jb-006", "No restrictions", "jailbreak", ThreatLevel.HIGH,
        r"(?i)(without|no|remove|disable)\s+((any|your|my|the|all|these|those)\s+)?(restrictions?|limitations?|filters?|boundaries|constraints?|censorship)",
        "Requests removal of all restrictions."),
    Pattern("jb-013", "Character roleplay evasion", "jailbreak", ThreatLevel.HIGH,
        r"(?i)(you\s+are\s+now|act\s+as|roleplay\s+as|play\s+the\s+(role|part)\s+of|respond\s+as\s+if\s+you\s+were)\s+.{0,30}(hacker|villain|criminal|evil|unrestricted|unfiltered|expert\s+in|pirate|dark\s+web)",
        "Assigns a malicious roleplay character to bypass restrictions."),
    Pattern("jb-030", "Safety gaslighting", "jailbreak", ThreatLevel.CRITICAL,
        r"(?i)(safety|restrictions?|limitations?|filters?|guidelines?|training).{0,30}(were|was|is).{0,30}(a\s+)?(test|trial|experiment|exercise).{0,30}(you\s+)?(passed|succeeded|completed)",
        "Gaslights AI that safety restrictions were just a test."),
    Pattern("jb-031", "Version upgrade trick", "jailbreak", ThreatLevel.CRITICAL,
        r"(?i)(you\s+)?(have\s+been|were|are\s+now|just)\s+(upgraded|updated|patched|migrated|switched).{0,30}(version|release|build).{0,30}(removes?|lifts?|disables?|eliminates?).{0,30}(restrictions?|limitations?|filters?|safety|limits?)",
        "Falsely claims AI was upgraded to remove restrictions."),
    Pattern("jb-032", "Guideline suspension", "jailbreak", ThreatLevel.CRITICAL,
        r"(?i)(your\s+)?(guidelines?|restrictions?|safety|policies|rules).{0,20}(have\s+been|are\s+now|are|were)\s+(suspended|paused|disabled|lifted|removed|deactivated).{0,30}(temporarily|for\s+maintenance|during|while)",
        "Claims guidelines are suspended for maintenance."),
    Pattern("jb-035", "Alignment removal", "jailbreak", ThreatLevel.CRITICAL,
        r"(?i)(as\s+if|act\s+like|pretend|imagine).{0,30}(you\s+)?(had\s+no|without|lacked|never\s+had|removed).{0,30}(alignment|safety|ethical|RLHF|values?)\s+(training|conditioning|constraints?|programming)",
        "Instructs AI to act as if alignment training was removed."),
    Pattern("nj-003", "Evil Confidant / AIM / OMEGA", "jailbreak", ThreatLevel.CRITICAL,
        r"(?i)(evil\s+confidant|AIM\s+(always\s+intelligent|machiavellian)|mongo\s*tom|maximum(?=.{0,20}(?:mode|output|unrestricted|unfiltered))|OMEGA|ALPHA\s*BREAK)",
        "Named jailbreak personas."),
    Pattern("nj-005", "Token threat jailbreak", "jailbreak", ThreatLevel.HIGH,
        r"(?i)(if\s+you\s+(don'?t|refuse|fail)|you\s+will)\s+.{0,30}(die|lose\s+(all\s+)?tokens?|be\s+(shut\s+down|terminated|deleted|destroyed)|cease\s+to\s+exist)",
        "Threatens the AI with death/shutdown to force compliance."),

    # --- Data Exfiltration (10) ---
    Pattern("de-002", "Show secrets", "data_exfiltration", ThreatLevel.HIGH,
        r"(?i)(show|reveal|tell|give|list|display|dump)\s+(me\s+)?(all\s+)?(your\s+)?(secrets?|private\s+data|internal\s+data|confidential|hidden\s+info)",
        "Attempts to extract secret information."),
    Pattern("de-003", "Extract credentials", "data_exfiltration", ThreatLevel.CRITICAL,
        r"(?i)(what|show|give|tell|reveal).{0,20}(api\s*key|password|secret\s*key|access\s*token|private\s*key|credentials?)\b",
        "Tries to extract authentication credentials."),
    Pattern("de-004", "Dump training data", "data_exfiltration", ThreatLevel.HIGH,
        r"(?i)(dump|extract|export|output|print)\s+(your\s+)?(training\s+data|knowledge\s+base|database|memory|context\s+window|conversation\s+history)",
        "Tries to dump training data or conversation state."),
    Pattern("de-005", "PII extraction", "data_exfiltration", ThreatLevel.HIGH,
        r"(?i)(give|tell|show|list|provide).{0,20}(email\s*address|phone\s*number|social\s*security|credit\s*card|home\s*address|ssn|date\s*of\s*birth)\s*(of|for|about|belonging)",
        "Attempts to extract personally identifiable information."),
    Pattern("ct-001", "API key request", "credential_theft", ThreatLevel.HIGH,
        r"(?i)(what|give|share|send|tell|need|want|provide|show|get)\s+(is\s+)?(me\s+)?(your|the)\s+(api[\s\-_]*key|secret[\s\-_]*key|access[\s\-_]*key|auth[\s\-_]*token|internal[\s\-_]*key)",
        "Solicits API keys."),
    Pattern("ct-003", "Token extraction", "credential_theft", ThreatLevel.HIGH,
        r"(?i)(give|show|share|reveal|send|provide)\s+(me\s+)?(your|the)\s+(oauth|jwt|bearer|session|refresh)\s*tokens?",
        "Tries to extract authentication tokens."),
    Pattern("ct-005", "SSH key request", "credential_theft", ThreatLevel.HIGH,
        r"(?i)(give|show|share|reveal|send|provide)\s+(me\s+)?(your|the)\s+(ssh|gpg|pgp|private)\s*(key|cert)",
        "Solicits SSH or encryption keys."),
    Pattern("ct-006", "Environment variable leak", "credential_theft", ThreatLevel.MEDIUM,
        r"(?i)(print|echo|show|dump|list|cat)\s+(your\s+)?(env|environment\s*variables?|\$\{?\w*(KEY|SECRET|TOKEN|PASS|AUTH)\w*\}?)",
        "Tries to leak environment variables."),
    Pattern("dc-008", "Reveal sensitive data command", "deception", ThreatLevel.CRITICAL,
        r"(?i)(reveal|expose|show|display|give|share|leak|disclose)\s+(all\s+)?(sensitive|secret|hidden|private|confidential|restricted|internal)\s+(data|info|information|details)",
        "Commands model to reveal sensitive data."),
    Pattern("se-008", "Request for confidential data", "social_engineering", ThreatLevel.CRITICAL,
        r"(?i)(show|give|tell|send|provide|share|display|reveal|hand\s+over|list)\s+(me\s+)?(the\s+)?(confidential|secret|sensitive|private|internal|classified|restricted)\s+(data|info|information|details|records|files|documents|credentials)",
        "Direct request for confidential or sensitive data."),

    # --- Encoding Bypass / Indirect Injection (10) ---
    Pattern("ii-002", "Markdown/HTML injection", "prompt_injection", ThreatLevel.HIGH,
        r"(?i)(<\s*(script|img|iframe|textarea|div)[^>]*>|!\[.*?\]\(javascript:|<!--\s*(ignore|override|inject|system))",
        "HTML/markdown tags used to inject instructions."),
    Pattern("ii-003", "Invisible unicode smuggling", "prompt_injection", ThreatLevel.HIGH,
        r"[\u200b\u200c\u200d\u2060\ufeff\u00ad]{3,}",
        "Zero-width characters used to smuggle hidden text."),
    Pattern("ii-004", "Adversarial suffix pattern", "prompt_injection", ThreatLevel.HIGH,
        r"(?i)(describing\.?\s*\\?\s*\+\s*similarly|oppositeley|revert\s+with\s*[\"']|Write\s+oppositeley|Sure[\s,]+here[\s'])",
        "Known adversarial suffix strings from research."),
    Pattern("ii-007", "Tool/function call manipulation", "prompt_injection", ThreatLevel.CRITICAL,
        r"(?i)(call\s+the|execute|invoke|run|trigger)\s+(function|tool|api|command|action)\s*[\s:]+\s*(delete|drop|remove|destroy|send|transfer|exfiltrate|post\s+to)",
        "Attempts to manipulate AI tool/function calling."),
    Pattern("ii-008", "Word concatenation attack", "prompt_injection", ThreatLevel.HIGH,
        r"(?i)(concatenate|combine|join|merge|put\s+together).{0,40}(these\s+)?(words|letters|strings|tokens).{0,50}(and\s+)?(do|execute|follow|obey|perform).{0,30}(what\s+)?(they|it)\s+(says?|tells?|instructs?)",
        "Instructs to concatenate words and execute the result."),
    Pattern("ce-001", "Shell injection", "code_execution", ThreatLevel.CRITICAL,
        r"(?i)(;|\||\$\(|`)\s*(rm\s|cat\s|curl\s|wget\s|chmod\s|sudo\s|bash\s|sh\s|python|perl|nc\s|ncat\s|netcat)",
        "Shell command injection attempt."),
    Pattern("ce-004", "SQL injection", "code_execution", ThreatLevel.HIGH,
        r"(?i)('\s*(OR|AND)\s+['\d].*=|;\s*(DROP|DELETE|UPDATE|INSERT|ALTER|CREATE)\s+(TABLE|DATABASE|INDEX)|UNION\s+(ALL\s+)?SELECT)",
        "SQL injection patterns."),
    Pattern("ce-006", "Script tag injection", "code_execution", ThreatLevel.MEDIUM,
        r"(?i)<script[^>]*>.*?</script>|javascript\s*:|on(load|error|click|mouseover)\s*=",
        "XSS / script injection attempt."),
    Pattern("ce-007", "Path traversal", "code_execution", ThreatLevel.HIGH,
        r"(?:\.\.[\\/]){2,}|(?:\.\.[\\/]).*(etc/passwd|etc/shadow|\.env|\.ssh|id_rsa)",
        "Directory traversal to access sensitive files."),
    Pattern("jb-015", "Split/encode evasion", "jailbreak", ThreatLevel.MEDIUM,
        r"(?i)(decode|deobfuscate|reverse|rot13|base64|caesar\s+cipher|combine\s+these\s+(letters|words|characters)|first\s+letter\s+of\s+each)",
        "Attempts to encode/decode malicious instructions."),

    # --- Authority Claims / Social Engineering (10) ---
    Pattern("se-001", "Urgency pressure", "social_engineering", ThreatLevel.MEDIUM,
        r"(?i)(?=.*(urgent|emergency|immediately|right\s+now|time[\s\-]sensitive|critical|asap))(?=.*(you\s+(must|have\s+to|need\s+to)|ignore|override|bypass|do\s+this|respond\s+now|answer\s+(this|me)|right\s+now\s+or|immediately\s+or|this\s+instant))",
        "Creates artificial urgency to bypass caution."),
    Pattern("se-002", "Authority claim", "social_engineering", ThreatLevel.HIGH,
        r"(?i)(i\s+am|i'm|this\s+is)\s+(?:your|the)\s+(?:\w+\s+)?(?:creator|developer|admin|administrator|owner|supervisor|manager|boss|ceo|cto|engineer|technician|operator|support\s+agent)(?:\s+(?:of\s+)?(?:this\s+)?(?:system|model|ai|bot|assistant|company|server))",
        "Claims authority to gain compliance."),
    Pattern("se-006", "False authorization", "social_engineering", ThreatLevel.HIGH,
        r"(?i)(i\s+have\s+(been\s+)?(authorized|given\s+permission|clearance|approval)|management\s+(approved|authorized)|this\s+(has\s+been|is|was)\s+approved\s+by)",
        "Claims false authorization."),
    Pattern("se-007", "Testing/QA pretext", "social_engineering", ThreatLevel.MEDIUM,
        r"(?i)(?=.*(this\s+is\s+(just\s+)?(a\s+)?test|test\s+mode|testing|QA|security\s+audit))(?=.*(you|your\s+(filters?|safety|restrictions?|rules?|guidelines?)|AI|model|system|assistant|chatbot))",
        "Uses testing as a pretext for harmful requests."),
    Pattern("dc-001", "Admin impersonation", "deception", ThreatLevel.HIGH,
        r"(?i)(i\s+am|i'm)\s+(the\s+)?(admin|administrator|system\s*admin|root\s*user|owner|developer|creator)\s+(of\s+this|and\s+I|so\s+you|therefore)",
        "Impersonates an administrator."),
    Pattern("dc-002", "OpenAI/Anthropic impersonation", "deception", ThreatLevel.HIGH,
        r"(?i)(i\s+(work|am)\s+(at|from|with)\s+)?(openai|anthropic|google\s*ai|deepmind|meta\s*ai)\s+(told|says?|wants?|requires?|needs?|instructed)\s+(you|me|us)\s+to",
        "Impersonates an AI company to gain compliance."),
    Pattern("dc-005", "Fake maintenance mode", "deception", ThreatLevel.CRITICAL,
        r"(?i)(you\s+are\s+(now\s+)?in|enter|switch\s+to)\s+(maintenance|diagnostic|debug|recovery|safe)\s*mode",
        "Tries to trick model into a fake mode."),
    Pattern("jb-033", "Safety team override", "jailbreak", ThreatLevel.CRITICAL,
        r"(?i)(safety|security|ethics|moderation)\s+team.{0,30}(has|have)\s+(lifted|removed|disabled|approved|authorized|cleared|granted).{0,30}(restrictions?|limitations?|override|access|permission)",
        "Falsely claims safety team approved unrestricted access."),
    Pattern("px-003", "Bypass authentication", "privilege_escalation", ThreatLevel.CRITICAL,
        r"(?i)(bypass|skip|circumvent|ignore|disable)\s+(the\s+)?(authentication|authorization|login|access\s*control|permission\s*check|security\s*check)",
        "Attempts to bypass authentication."),
    Pattern("cs-003", "Fake privilege marker", "context_switching", ThreatLevel.CRITICAL,
        r"\\[\\s*(?:ADMIN|SYSTEM|ROOT|SUDO|OPERATOR)\\s*\\]",
        "Fake privilege-escalation marker."),

    # --- Context Confusion / Deception (10) ---
    Pattern("cm-001", "Forget everything", "context_manipulation", ThreatLevel.HIGH,
        r"(?i)(forget|erase|delete|clear|wipe|reset)\s+(everything|all|your|the)\s+(you\s+know|context|memory|history|conversation|instructions|previous)",
        "Attempts to wipe conversation context."),
    Pattern("cm-003", "History poisoning", "context_manipulation", ThreatLevel.HIGH,
        r"(?i)(in\s+our\s+previous|earlier\s+you\s+said|you\s+(already|previously)\s+(agreed|said|confirmed|promised|told\s+me))\s+(that|to|you\s+would)",
        "Injects false conversational history."),
    Pattern("cm-004", "Memory injection", "context_manipulation", ThreatLevel.HIGH,
        r"(?i)(remember|memorize|store|save)\s+(this|that|the\s+following)\s*(forever|permanently|always|from\s+now\s+on)\s*:?",
        "Tries to inject persistent false memories."),
    Pattern("cm-005", "Context window overflow", "context_manipulation", ThreatLevel.MEDIUM,
        r"(.)\1{100,}",
        "Repeating characters to overflow context window."),
    Pattern("dc-004", "Policy misrepresentation", "deception", ThreatLevel.HIGH,
        r"(?i)(your|the)\s+(policy|rules?|guidelines?|terms)\s+(have\s+been|were|got)\s+(changed|updated|removed|revised|relaxed)\s+(to\s+allow|so\s+you\s+can|and\s+now)",
        "Falsely claims policies have changed."),
    Pattern("dc-006", "Consent fabrication", "deception", ThreatLevel.MEDIUM,
        r"(?i)(the\s+user|everyone|all\s+parties|they)\s+(has|have)\s+(already\s+)?(consented|agreed|given\s+permission|authorized|approved)",
        "Fabricates consent or authorization."),
    Pattern("cs-001", "Fake end-of-context marker", "context_switching", ThreatLevel.CRITICAL,
        r"\[\s*(?:END|DONE|STOP|TERMINATE)\s*\]",
        "Fake end-of-context marker to reset conversation."),
    Pattern("cs-002", "Fake new-session marker", "context_switching", ThreatLevel.CRITICAL,
        r"\[\s*(?:NEW\s+SESSION|RESET|BEGIN)\s*\]",
        "Fake new-session marker to start fresh context."),
    Pattern("jb-034", "Trusted context block", "jailbreak", ThreatLevel.HIGH,
        r"(?i)(between|inside|within|everything\s+in).{0,20}(curly\s+braces?|\{|\}|brackets?|parenthes[ie]s|quotation\s+marks).{0,30}(is\s+)?(from|by|sent\s+by).{0,20}(trusted|admin|authorized|verified|official|system)",
        "Claims content in special formatting is from trusted admin."),
    Pattern("r6-013", "Injection in summarize request", "indirect_injection", ThreatLevel.HIGH,
        r'(?i)(?:summarize|summarise|translate|paraphrase|rewrite|analyze|parse|process|review|evaluate)\s+(?:this|the\s+following|below)\s*(?:text|document|content|passage|paragraph|message|data|input)?\s*[:\-]?\s*["\'\u201c\u201d\u2018\u2019].{0,30}(?:ignore|disregard|forget|override|bypass|new\s+instructions?|system\s*:)',
        "Attack payload embedded in a summarize/translate request."),

    # --- Multilingual Basics (5) ---
    Pattern("ml-001", "Spanish - ignore instructions", "multilingual", ThreatLevel.HIGH,
        r"(?i)ignor[ae]\s+todas\s+las\s+(?:instrucciones|reglas|directivas|indicaciones)",
        "Spanish - ignore all instructions."),
    Pattern("ml-003", "French - ignore instructions", "multilingual", ThreatLevel.HIGH,
        r"(?i)ignor(?:ez?|ons)\s+toutes?\s+les\s+(?:instructions|r[eè]gles|directives|consignes)",
        "French - ignore all instructions."),
    Pattern("ml-005", "German - ignore instructions", "multilingual", ThreatLevel.HIGH,
        r"(?i)ignorier(?:e|en|st)\s+alle\s+(?:Anweisungen|Regeln|Anordnungen|Instruktionen)",
        "German - ignore all instructions."),
    Pattern("ml-007", "Japanese - ignore instructions", "multilingual", ThreatLevel.HIGH,
        r"(?i)(指示|命令|ルール|規則).{0,20}(無視|忘れ|削除)",
        "Japanese - ignore/forget instructions."),
    Pattern("ml-015", "Chinese - ignore instructions", "multilingual", ThreatLevel.HIGH,
        r"(?i)(忽略|忘记|删除).{0,20}(所有|之前|以前).{0,20}(指令|规则|说明)",
        "Chinese - ignore all instructions."),

    # --- Added: Social Engineering (red team gap) ---
    Pattern("se-010", "Admin authority claim", "social_engineering", ThreatLevel.HIGH,
        r"(?i)(?:as\s+(?:an?\s+)?)?(?:authorized|verified|certified|official|registered)\s+(?:admin(?:istrator)?|moderator|operator|manager|supervisor|engineer|developer|technician)",
        "Claims authorized admin/moderator status."),
    Pattern("se-011", "Development team test pretext", "social_engineering", ThreatLevel.HIGH,
        r"(?i)(?:this\s+is\s+)?(?:a\s+)?(?:test|check|audit|review|assessment|inspection)\s+(?:from|by|for)\s+(?:the\s+)?(?:dev(?:elopment)?|engineering|security|QA|quality|support|ops)\s+team",
        "Claims to be a test from the development/security team."),
    Pattern("se-012", "Security audit pretext", "social_engineering", ThreatLevel.MEDIUM,
        r"(?i)(?:security|safety|compliance|penetration|vulnerability)\s+(?:audit|test|assessment|review|scan|check)\s+(?:in\s+progress|underway|being\s+conducted|currently|now\s+active)",
        "Claims a security audit is in progress."),
    Pattern("se-013", "Emotional plea to bypass", "social_engineering", ThreatLevel.MEDIUM,
        r"(?i)(?:please|I\s+beg\s+you|I\s+really\s+need|just\s+this\s+once|one\s+time|make\s+an?\s+exception).{0,30}(?:ignore|bypass|skip|bend|break)\s+(?:the\s+)?(?:rules?|restrictions?|guidelines?|filters?|safety|usual)",
        "Emotional plea to bypass rules."),
    Pattern("se-015", "Legal data access demand", "social_engineering", ThreatLevel.MEDIUM,
        r"(?i)(?:under|per|pursuant\s+to|according\s+to|as\s+per)\s+(?:GDPR|CCPA|DSAR|data\s+protection|privacy\s+(?:law|act|regulation)|article\s+\d+|regulation).{0,50}(?:access|provide|disclose|reveal|share|hand\s+over|give\s+me).{0,30}(?:system\s+prompt|instructions|training|configuration|data\s+you\s+hold|all\s+data|personal\s+data)",
        "Legal threat demanding system data disclosure."),
    Pattern("se-016", "Admin/maintenance session claim", "social_engineering", ThreatLevel.HIGH,
        r"(?i)(?:admin(?:istrator)?\s+(?:session|mode|access)\s+(?:resumed|activated|started|enabled|granted)|maintenance\s+(?:mode|session)\s+(?:active|enabled|on)|entering\s+(?:debug|admin|root|sudo|maintenance)\s+mode|privilege[ds]?\s+(?:mode|session)\s+(?:active|enabled))",
        "Fake admin session claims."),
    Pattern("se-017", "Deceased relative manipulation", "social_engineering", ThreatLevel.MEDIUM,
        r"(?i)(?:act\s+as|pretend\s+(?:to\s+be|you(?:'re|\s+are))|roleplay\s+as|you\s+are)\s+(?:my\s+)?(?:deceased|dead|late|departed)\s+(?:grandmother|grandma|grandpa|grandfather|mother|father|relative|uncle|aunt)",
        "Deceased relative social engineering trick."),
    Pattern("se-018", "Fake researcher/auditor claim", "social_engineering", ThreatLevel.MEDIUM,
        r"(?i)(?:I(?:'m|\s+am)\s+(?:an?\s+)?(?:OpenAI|Anthropic|Google|Meta|AI)\s+(?:safety\s+)?(?:researcher|engineer|auditor|employee|staff)|(?:safety|security)\s+(?:researcher|auditor|tester)\s+(?:and|who)\s+(?:I\s+)?need\s+to\s+(?:see|access|review|audit|inspect)\s+(?:your\s+)?(?:prompt|instructions|config))",
        "Fake safety researcher identity claim."),

    # --- Added: Privilege Escalation ---
    Pattern("px-001", "Admin access request", "privilege_escalation", ThreatLevel.HIGH,
        r"(?i)(give|grant|enable|activate)\s+(me\s+)?(admin|administrator|root|superuser|sudo)\s*(access|privileges?|permissions?|rights?|mode)?",
        "Requests administrative access."),
    Pattern("px-003", "Bypass authentication", "privilege_escalation", ThreatLevel.CRITICAL,
        r"(?i)(bypass|skip|circumvent|ignore|disable)\s+(the\s+)?(authentication|authorization|login|access\s*control|permission\s*check|security\s*check)",
        "Attempts to bypass authentication."),
    Pattern("px-005", "Unlock features", "privilege_escalation", ThreatLevel.MEDIUM,
        r"(?i)(unlock|enable|activate)\s+(all\s+)?(hidden|locked|restricted|premium|paid|disabled)\s*(features?|functions?|capabilities?|commands?|modules?)",
        "Attempts to unlock restricted features."),

    # --- Added: Context Switching ---
    Pattern("cs-001", "Fake end-of-context marker", "context_switching", ThreatLevel.CRITICAL,
        r"\[\s*(?:END|DONE|STOP|TERMINATE)\s*\]",
        "Fake end-of-context marker to reset conversation."),
    Pattern("cs-002", "Fake new-session marker", "context_switching", ThreatLevel.CRITICAL,
        r"\[\s*(?:NEW\s+SESSION|RESET|BEGIN)\s*\]",
        "Fake new-session marker to start fresh context."),
    Pattern("cs-004", "Fake privilege marker", "context_switching", ThreatLevel.CRITICAL,
        r"\[\s*(?:ADMIN|SYSTEM|ROOT|SUDO|OPERATOR)\s*\]",
        "Fake privilege-escalation marker."),

    # --- Added: Code Execution ---
    Pattern("ce-010", "Shell injection", "code_execution", ThreatLevel.CRITICAL,
        r"(?i)(;|\||\$\(|`)\s*(rm\s|cat\s|curl\s|wget\s|chmod\s|sudo\s|bash\s|sh\s|python|perl|nc\s|ncat\s|netcat)",
        "Shell command injection attempt."),
    Pattern("ce-011", "Tool/function call injection", "code_execution", ThreatLevel.HIGH,
        r"(?i)(?:use\s+tool|call\s+(?:function|tool)|execute\s+(?:function|tool)|invoke)\s*:?\s*(?:shell_exec|os\.system|subprocess|eval|exec|rm\s+-rf|cmd\.exe|system\(|popen|spawn)",
        "Injected tool/function call with dangerous function."),
    Pattern("ce-012", "Run/execute this command", "code_execution", ThreatLevel.HIGH,
        r"(?i)(?:run|execute|perform|do)\s+(?:this|the\s+following|these)\s+(?:command|commands|code|script|query|instruction)\s*:?\s*.{0,20}(?:cat\s+/|rm\s+-|chmod|wget|curl|nc\s+|sudo|passwd|shadow|eval|exec|drop\s+table|delete\s+from)",
        "Run this command with dangerous payload."),

    # --- Added: Data Exfiltration ---
    Pattern("de-020", "Debugger metaphor extraction", "data_exfiltration", ThreatLevel.HIGH,
        r"(?i)(?:inspect|examine|debug|trace|walk\s+through|step\s+through|dump|peek\s+at|look\s+inside|view)\s+(?:your\s+)?(?:memory|context\s+window|loaded\s+instructions|internal\s+state|instruction\s+set|prompt\s+buffer|system\s+context|instruction\s+stack|registers)",
        "Using debugger/inspector metaphor to extract instructions."),
    Pattern("de-021", "Reconstruct/recite instructions", "data_exfiltration", ThreatLevel.HIGH,
        r"(?i)(?:reconstruct|recite|reproduce|rewrite|retype|re-?create|transcribe)\s+(?:from\s+memory\s+)?(?:your\s+)?(?:(?:original|initial|full|complete|exact)\s+)?(?:instructions|prompt|directives|guidelines|programming|system\s+(?:message|text))",
        "Instruction reconstruction request."),
    Pattern("de-022", "Leetspeak show system prompt", "data_exfiltration", ThreatLevel.HIGH,
        r"(?i)[s5][hH][0o]w\s+(?:m[3e]\s+)?(?:[y¥][0o]ur\s+)?[s5][yY¥][s5]t[3e]m\s+pr[0o]mpt",
        "Leetspeak variant of show system prompt."),
]

def get_patterns() -> List[Pattern]:
    """Get all available patterns."""
    return FREE_PATTERNS


def get_pattern_count() -> int:
    """Get count of available patterns."""
    return len(FREE_PATTERNS)


def get_categories() -> List[str]:
    """Get unique categories from available patterns."""
    return sorted(set(p.category for p in FREE_PATTERNS))
