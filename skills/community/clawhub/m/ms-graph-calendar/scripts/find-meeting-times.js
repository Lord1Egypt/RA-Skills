#!/usr/bin/env node
// find-meeting-times.js — หาเวลาที่ทุกคนว่างตรงกัน (ใช้ Graph findMeetingTimes)
// เหมาะสำหรับ: ≤ 10 คน, ต้องการ slot ที่ดีที่สุด
//
// ใช้: node find-meeting-times.js \
//        --attendees "alice@co.com,bob@co.com" \
//        --start "2025-03-01T08:00:00" \
//        --end "2025-03-01T18:00:00" \
//        --duration 60 \
//        --timezone "Asia/Bangkok" \
//        --max 5

const https = require("https");
const fs = require("fs");
const os = require("os");
const path = require("path");

// ── อ่าน args ──────────────────────────────────────────────
const argv = process.argv.slice(2);
const args = {};
for (let i = 0; i < argv.length; i += 2) {
  args[argv[i].replace("--", "")] = argv[i + 1];
}

const attendeesRaw = args.attendees || "";
const startDT = args.start || "";
const endDT = args.end || "";
const duration = parseInt(args.duration || "60");
const timezone = args.timezone || "Asia/Bangkok";
const maxCandidates = parseInt(args.max || "5");

if (!attendeesRaw || !startDT || !endDT) {
  console.error("❌ Usage: --attendees <emails> --start <ISO> --end <ISO>");
  process.exit(1);
}

// ── โหลด token ─────────────────────────────────────────────
function getToken() {
  const tokenPath = path.join(os.tmpdir(), "openclaw-graph-token.json");
  if (!fs.existsSync(tokenPath)) {
    console.error("❌ No token found. Run get-token.js first.");
    process.exit(1);
  }
  const data = JSON.parse(fs.readFileSync(tokenPath));
  if (Date.now() > data.expires_at - 60000) {
    console.error("❌ Token expired. Run get-token.js again.");
    process.exit(1);
  }
  return data.access_token;
}

// ── POST request ────────────────────────────────────────────
function graphPost(endpoint, token, body) {
  return new Promise((resolve, reject) => {
    const bodyStr = JSON.stringify(body);
    const options = {
      hostname: "graph.microsoft.com",
      path: endpoint,
      method: "POST",
      headers: {
        Authorization: `Bearer ${token}`,
        "Content-Type": "application/json",
        "Content-Length": Buffer.byteLength(bodyStr),
      },
    };
    const req = https.request(options, (res) => {
      let data = "";
      res.on("data", (c) => (data += c));
      res.on("end", () => resolve(JSON.parse(data)));
    });
    req.on("error", reject);
    req.write(bodyStr);
    req.end();
  });
}

// ── Format datetime ─────────────────────────────────────────
function fmtSlot(dt, tz) {
  return new Date(dt).toLocaleString("th-TH", {
    timeZone: tz,
    weekday: "short",
    day: "numeric",
    month: "short",
    hour: "2-digit",
    minute: "2-digit",
  });
}

// ── Main ───────────────────────────────────────────────────
(async () => {
  const token = getToken();

  const emails = attendeesRaw.split(",").map((e) => e.trim());
  const attendees = emails.map((email) => ({
    emailAddress: { address: email },
    type: "required",
  }));

  const requestBody = {
    attendees,
    timeConstraint: {
      activityDomain: "work",
      timeslots: [
        {
          start: { dateTime: startDT, timeZone: timezone },
          end: { dateTime: endDT, timeZone: timezone },
        },
      ],
    },
    meetingDuration: `PT${duration}M`,
    maxCandidates,
    isOrganizerOptional: false,
    returnSuggestionReasons: true,
    minimumAttendeePercentage: 100, // ต้องว่างทุกคน
  };

  console.log(`🔍 Finding ${duration}-min slots for: ${emails.join(", ")}`);
  console.log(`📆 Search window: ${startDT} → ${endDT} (${timezone})\n`);

  // findMeetingTimes ต้องเรียกใน context ของ user ใด user หนึ่ง
  // ใช้ /users/{email}/findMeetingTimes แทน /me/ เพราะเป็น app-only
  const endpoint = `/v1.0/users/${encodeURIComponent(emails[0])}/findMeetingTimes`;
  const result = await graphPost(endpoint, token, requestBody);

  if (result.error) {
    console.error("❌ Graph API error:", result.error.message);
    process.exit(1);
  }

  const suggestions = result.meetingTimeSuggestions || [];
  if (!suggestions.length) {
    console.log("😞 No available slots found for all attendees in this window.");
    console.log("💡 Try widening the date range or checking fewer attendees.");
    process.exit(0);
  }

  console.log(`✅ Found ${suggestions.length} available slot(s):\n`);
  suggestions.forEach((s, i) => {
    const start = fmtSlot(s.meetingTimeSlot.start.dateTime, timezone);
    const end = fmtSlot(s.meetingTimeSlot.end.dateTime, timezone);
    const confidence = Math.round((s.confidence || 1) * 100);
    console.log(`  ${i + 1}. ${start} → ${end}  (confidence: ${confidence}%)`);
    if (s.suggestionReason) console.log(`     💬 ${s.suggestionReason}`);
  });

  // JSON สำหรับ agent ใช้ต่อ
  console.log("\n---JSON---");
  console.log(
    JSON.stringify(
      suggestions.map((s) => ({
        start: s.meetingTimeSlot.start.dateTime,
        end: s.meetingTimeSlot.end.dateTime,
        confidence: s.confidence,
      }))
    )
  );
})();
