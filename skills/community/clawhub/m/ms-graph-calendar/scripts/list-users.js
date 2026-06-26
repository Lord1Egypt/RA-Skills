#!/usr/bin/env node
// list-users.js — ค้นหาพนักงานตามชื่อหรือกลุ่ม
// ใช้: node list-users.js --search "Alice"
//       node list-users.js --group "Marketing"
//       node list-users.js  (ดึงทั้งหมด, จำกัด 100 คน)

const https = require("https");
const fs = require("fs");
const os = require("os");
const path = require("path");

// ── อ่าน args ──────────────────────────────────────────────
const args = Object.fromEntries(
  process.argv.slice(2).reduce((acc, val, i, arr) => {
    if (val.startsWith("--")) acc.push([val.slice(2), arr[i + 1]]);
    return acc;
  }, [])
);

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

// ── เรียก Graph API ────────────────────────────────────────
function graphGet(endpoint, token) {
  return new Promise((resolve, reject) => {
    const url = new URL("https://graph.microsoft.com" + endpoint);
    const options = {
      hostname: url.hostname,
      path: url.pathname + url.search,
      headers: { Authorization: `Bearer ${token}`, "Content-Type": "application/json" },
    };
    https.get(options, (res) => {
      let data = "";
      res.on("data", (c) => (data += c));
      res.on("end", () => resolve(JSON.parse(data)));
    }).on("error", reject);
  });
}

// ── Main ───────────────────────────────────────────────────
(async () => {
  const token = getToken();
  let endpoint;

  if (args.group) {
    // ค้นกลุ่มก่อน แล้วดึง members
    const groups = await graphGet(
      `/v1.0/groups?$filter=startswith(displayName,'${encodeURIComponent(args.group)}')&$select=id,displayName`,
      token
    );
    if (!groups.value?.length) {
      console.log(`❌ No group found matching "${args.group}"`);
      process.exit(0);
    }
    const groupId = groups.value[0].id;
    const groupName = groups.value[0].displayName;
    console.log(`📂 Group: ${groupName}`);

    const members = await graphGet(
      `/v1.0/groups/${groupId}/members?$select=displayName,mail,id`,
      token
    );
    const users = (members.value || []).filter((u) => u.mail);
    printUsers(users);
  } else if (args.search) {
    endpoint = `/v1.0/users?$filter=startswith(displayName,'${encodeURIComponent(args.search)}') or startswith(mail,'${encodeURIComponent(args.search)}')&$select=displayName,mail,id&$top=10`;
    const result = await graphGet(endpoint, token);
    printUsers(result.value || []);
  } else {
    endpoint = `/v1.0/users?$select=displayName,mail,id&$top=100&$orderby=displayName`;
    const result = await graphGet(endpoint, token);
    printUsers(result.value || []);
  }
})();

function printUsers(users) {
  if (!users.length) {
    console.log("❌ No users found.");
    return;
  }
  console.log(`\n👥 Found ${users.length} user(s):\n`);
  users.forEach((u, i) => {
    console.log(`  ${i + 1}. ${u.displayName} — ${u.mail}`);
  });
  // JSON สำหรับ agent ใช้ต่อ
  console.log("\n---JSON---");
  console.log(JSON.stringify(users.map((u) => ({ name: u.displayName, email: u.mail }))));
}
