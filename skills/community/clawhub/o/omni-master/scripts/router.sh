#!/bin/bash
# omni router v3 — enhanced domain classifier with all modules
# Usage: ./router.sh "user query here"

QUERY="$1"

if [ -z "$QUERY" ]; then
    echo "Usage: ./router.sh \"query\""
    exit 1
fi

echo "=== OMNI Domain Router v3 ==="
echo "Query: $QUERY"
echo ""

MATCHES=0
declare -A MATCHED

classify() {
    local pattern="$1"
    local domain="$2"
    local file="$3"
    if [ -n "${MATCHED[$domain]}" ]; then return; fi
    if echo "$QUERY" | grep -qiE "$pattern"; then
        echo "  → [$domain] references/$file"
        MATCHED[$domain]=1
        MATCHES=$((MATCHES + 1))
    fi
}

# === META-SKILLS (check first for vague/ambiguous queries) ===
classify "think|reason|decide|problem|debug|error|crash|broken|issue|fail|stuck|fix.*it|help.*me|why|how|what.*wrong" "Reasoning" "reasoning.md"
classify "vague|unclear|interpret|prompt|better|improve|enhance|clarify|assum|refine" "Prompting" "advanced-prompting.md"
classify "ethic|safety|privacy|boundary|responsible|permission|consent|GDPR|anonym|protect" "Ethics" "ethics-safety.md"
classify "test|QA|review|validat|verif|quality|check|assert|spec|requirement" "QA" "quality-assurance.md"
classify "performance|optimi|fast|slow|profile|benchmark|speed|efficien|latency|throughput|cache" "Performance" "performance.md"
classify "research|verify|fact.check|source|find.out|look.up|search|confirm|proo" "Research" "research.md"

# === CORE DOMAINS ===
classify "workflow|pipeline|automat|cron|schedul|trigger|routine" "Automation" "automation.md"
classify "code|program|script|refactor|git|PR|commit|develop|function|class|import|module|repo|branch|merge|compile|build" "Coding" "coding.md"
classify "data|analy[sz]|SQL|query|database|CSV|chart|dashboard|pandas|dataframe|table|column|row|schema" "Data & DB" "data-databases.md"
classify "scrape|crawl|browse|fetch|URL|website|HTML|selenium|puppeteer|request|web.*page" "Web" "web-scraping.md"
classify "money|budget|invoice|financ|account|stock|crypto|payment|price|cost|revenue|profit|loan|interest|invest|tax|salary|expense" "Finance" "finance.md"
classify "secur|audit|firewall|vuln|encrypt|harden|password|auth|token|breach|threat|risk" "Security" "security.md"
classify "image|photo|generat|edit.*image|video|frame|screenshot|thumbnail|picture|render|visual|crop|resize" "Media" "media-generation.md"
classify "music|song|audio|sound|TTS|voice|podcast|speech|listen|speak|sing|instrument|playlist|volume" "Music/Audio" "music-audio.md"
classify "email|mail|inbox|SMS|chat|messag|notif|notify|alert" "Email/Messaging" "email-messaging.md"
classify "calendar|event|meeting|reminder|appoint|deadline|due.date" "Calendar" "calendar-scheduling.md"
classify "PDF|DOCX|document|spreadsheet|presentation|OCR|word.doc|excel|pptx|xlsx|paper|report.file" "Documents" "documents.md"
classify "translat|language|i18n|locale|multi.lang|spanish|french|german|chinese|japanese|arabic" "Translation" "translation.md"
classify "write|article|blog|essay|copy|content.writ|book|story|draft|compose|summar|paraphras|proofread|grammar|edit.*text" "Writing" "writing-content.md"
classify "project|task|board|kanban|milestone|sprint|todo|backlog|roadmap|tracker|manage.*project" "Projects" "project-management.md"
classify "deploy|CI|CD|Docker|kubernetes|vercel|railway|render|nginx|terraform|ansible|container|hosting|infra" "DevOps" "deployment-devops.md"
classify "smart.home|IoT|Hue|Sonos|light.*control|thermostat|camera.*home|sleep.*pod|sensor|home.auto" "IoT" "iot-smarthome.md"
classify "Discord|Telegram|Slack|WhatsApp|iMessage|Signal|tweet|twitter|social.*media|post.*online" "Comms" "communications.md"
classify "notes|wiki|knowledge|Notion|Obsidian|bookmark|reference|organiz|filing|catalog" "Knowledge" "knowledge-mgmt.md"
classify "system.admin|process.manage|disk|terminal|shell|linux|debian|apt.install|package.install|service|daemon|port.check" "SysAdmin" "system-admin.md"
classify "API|endpoint|REST|GraphQL|webhook|schema|swagger|route|HTTP|status.code" "API" "api-design.md"

# === EXPANDED DOMAINS ===
classify "data.type|statistic.basic|probability|visualiz|distribut|mean.*median|correlat|regression|sample|format.*data|JSON.parse|CSV.read|XML.parse" "Data Literacy" "data-literacy.md"
classify "math|calculat|equation|formula|algebra|geometry|trig|calculu|statistic|convert.*unit|number.*theory|compute|arithmetic|sum|average|percent|ratio" "Math" "math-engine.md"
classify "health|fitness|workout|nutrition|meal.*plan|diet|exercise|wellness|BMI|calori|gym|protein|sleep.track" "Health" "health-fitness.md"
classify "resume|CV|cover.letter|interview|career|job.apply|hiring|salary.negoti|professional.dev|LinkedIn" "Career" "career.md"
classify "teach|learn|study|quiz|flashcard|explain.*concept|tutor|education|course|lesson|homework|exam|spaced.repet" "Learning" "learning.md"
classify "DNS|SSH|VPN|cloud.server|AWS|Azure|GCP|network.config|tunnel|proxy|CDN|load.balanc|VPC|subnet|firewall.rule" "Network/Cloud" "network-cloud.md"
classify "creative|fiction|story|brainstorm|design.think|presentation|slide|pitch|rhetoric|persuas|world.build|character.dev" "Creative" "creative.md"
classify "multi.agent|orchestrat|collaborat|parallel.agent|spawn.agent|agent.chain|sub.agent|delegat.task" "Multi-Agent" "multi-agent.md"
classify "websocket|realtime|event.driven|message.queue|SSE|streaming|server.sent|pub.sub|webhook.receive|live.update|socket" "Realtime" "realtime.md"
classify "server|nginx|caddy|reverse.proxy|host.*website|domain.*config|systemd|service.manage" "SysAdmin" "system-admin.md"

# === FALLBACK ===
if [ "$MATCHES" -eq 0 ]; then
    echo "  → [Reasoning] references/reasoning.md (fallback)"
    echo "  → [Prompting] references/advanced-prompting.md (fallback: interpret intent)"
    echo ""
    echo "No specific domain matched. Using reasoning + prompting to interpret."
fi

echo ""
echo "Total domains: $MATCHES"
echo "Load matched reference(s) for detailed instructions."
