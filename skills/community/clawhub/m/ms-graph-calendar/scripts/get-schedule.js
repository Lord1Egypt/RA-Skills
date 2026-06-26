#!/usr/bin/env node
// get-schedule.js — ดู free/busy ของพนักงานหลายคนพร้อมกัน (ใช้ Graph getSchedule)
// เหมาะสำหรับ: ดูภาพรวม, คนจำนวนมาก
//
// ใช้: node get-schedule.js \
//        --emails "alice@co.com,bob@co.com,carol@co.com" \
//        --start "2025-03-01T00:00:00" \
//        --end "2025-03-07T00:00:00" \
//        --timezone "Asia/Bangkok" \
//        --interval 30

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

const emailsRaw = args.emails || "";
const startDT = args.start || "";
const endDT = args.end || "";
const timezone = args.timezone || "Asia/Bangkok";
const intervalMinutes = parseInt(args.interval || "30");

if (!emailsRaw || !startDT || !endDT) {
  console.error("❌ Usage: --emails <emails> --start <ISO> --end <ISO>");
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

// ── Status map ─────────────────────────────────────────────
const STATUS_EMOJI = {
  "0": "🟢", // free
  "1": "🟡", // tentative
  "2": "🔴", // busy
  "3": "🟠", // out of office
  "4": "⚫", // working elsewhere
};
const STATUS_LABEL = {
  "0": "free",
  "1": "tentative",
  "2": "busy",
  "3": "OOO",
  "4": "elsewhere",
};

// ── หา common free slots ────────────────────────────────────
function findCommonFreeSlots(schedules, intervalMinutes) {
  if (!schedules.length) return [];

  const slotCount = schedules[0].availabilityView?.length || 0;
  const freeSlots = [];
  let i = 0;

  while (i < slotCount) {
    const allFree = schedules.every((s) => s.availabilityView?.[i] === "0");
    if (allFree) {
      const startIdx = i;
      while (i < slotCount && schedules.every((s) => s.availabilityView?.[i] === "0")) i++;
      const durationMins = (i - startIdx) * intervalMinutes;
      freeSlots.push({ startSlot: startIdx, endSlot: i - 1, durationMins });
    } else {
      i++;
    }
  }
  return freeSlots;
}

function slotToTime(startDT, slotIndex, intervalMins) {
  const ms = new Date(startDT).getTime() + slotIndex * intervalMins * 60000;
  return new Date(ms).toISOString();
}

// ── Main ───────────────────────────────────────────────────
(async () => {
  const token = getToken();
  const emails = emailsRaw.split(",").map((e) => e.trim());

  // getSchedule รองรับสูงสุด 20 mailboxes ต่อ request
  const BATCH_SIZE = 20;
  let allSchedules = [];

  for (let i = 0; i < emails.length; i += BATCH_SIZE) {
    const batch = emails.slice(i, i + BATCH_SIZE);
    const body = {
      schedules: batch,
      startTime: { dateTime: startDT, timeZone: timezone },
      endTime: { dateTime: endDT, timeZone: timezone },
      availabilityViewInterval: intervalMinutes,
    };

    // เรียกในบริบทของ user คนแรกใน batch
    const endpoint = `/v1.0/users/${encodeURIComponent(batch[0])}/calendar/getSchedule`;
    const result = await graphPost(endpoint, token, body);

    if (result.error) {
      console.error("❌ Graph API error:", result.error.message);
      process.exit(1);
    }
    allSchedules = allSchedules.concat(result.value || []);
  }

  console.log(`📅 Schedule view: ${startDT} → ${endDT} (${timezone})`);
  console.log(`⏱  Interval: ${intervalMinutes} min | Attendees: ${emails.length}\n`);

  // แสดง availability ของแต่ละคน (สรุป)
  allSchedules.forEach((s) => {
    const view = s.availabilityView || "";
    const freeCount = (view.match(/0/g) || []).length;
    const totalCount = view.length;
    const freePct = Math.round((freeCount / totalCount) * 100);
    console.log(`  ${s.scheduleId}: ${freePct}% free`);

    // แสดง busy blocks
    (s.scheduleItems || []).forEach((item) => {
      const start = new Date(item.start.dateTime).toLocaleString("th-TH", {
        timeZone: timezone,
        weekday: "short",
        month: "short",
        day: "numeric",
        hour: "2-digit",
        minute: "2-digit",
      });
      const end = new Date(item.end.dateTime).toLocaleString("th-TH", {
        timeZone: timezone,
        hour: "2-digit",
        minute: "2-digit",
      });
      const emoji = item.status === "oof" ? "🟠" : item.status === "tentative" ? "🟡" : "🔴";
      const subject = item.subject ? ` — ${item.subject}` : "";
      console.log(`    ${emoji} ${start} → ${end}${subject}`);
    });
    console.log();
  });

  // หา common free slots
  const commonFree = findCommonFreeSlots(allSchedules, intervalMinutes);

  if (!commonFree.length) {
    console.log("😞 No common free slots found for all attendees in this window.");
  } else {
    const significant = commonFree.filter((s) => s.durationMins >= 30);
    console.log(`✅ Common free slots (all ${emails.length} attendees free simultaneously):\n`);
    significant.slice(0, 10).forEach((slot, i) => {
      const startISO = slotToTime(startDT, slot.startSlot, intervalMinutes);
      const endISO = slotToTime(startDT, slot.endSlot + 1, intervalMinutes);
      const startFmt = new Date(startISO).toLocaleString("th-TH", {
        timeZone: timezone,
        weekday: "short",
        month: "short",
        day: "numeric",
        hour: "2-digit",
        minute: "2-digit",
      });
      const endFmt = new Date(endISO).toLocaleString("th-TH", {
        timeZone: timezone,
        hour: "2-digit",
        minute: "2-digit",
      });
      console.log(`  ${i + 1}. ${startFmt} → ${endFmt}  (${slot.durationMins} min free)`);
    });
  }

  // JSON สำหรับ agent ใช้ต่อ
  console.log("\n---JSON---");
  console.log(
    JSON.stringify({
      schedules: allSchedules.map((s) => ({
        email: s.scheduleId,
        availabilityView: s.availabilityView,
        busySlots: s.scheduleItems?.map((item) => ({
          start: item.start.dateTime,
          end: item.end.dateTime,
          subject: item.subject,
          status: item.status,
        })),
      })),
      commonFreeSlots: commonFree
        .filter((s) => s.durationMins >= 30)
        .slice(0, 10)
        .map((slot) => ({
          start: slotToTime(startDT, slot.startSlot, intervalMinutes),
          end: slotToTime(startDT, slot.endSlot + 1, intervalMinutes),
          durationMins: slot.durationMins,
        })),
    })
  );
})();
