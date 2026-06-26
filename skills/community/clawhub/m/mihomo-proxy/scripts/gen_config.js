/**
 * Mihomo 配置生成器 - 从订阅链接生成 config.yaml
 * 
 * 用法: node gen_config.js [订阅URL]
 *   - 不传URL: 使用上次的 /tmp/sub_raw.txt
 *   - 传URL: 自动下载并生成
 * 
 * 支持协议: vless (reality), hysteria2, trojan (ws)
 * 自动按地区分组: 日本/美国/香港/台湾/新加坡/韩国/英国/荷兰/德国/其他
 */

const fs = require('fs');
const { execSync } = require('child_process');

const SUB_FILE = '/tmp/sub_raw.txt';
const CONFIG_PATH = '/opt/mihomo-config/config.yaml';

function decodeName(name) {
  try { return decodeURIComponent(name); } catch { return name; }
}

function parseNode(line) {
  if (line.startsWith('hysteria2://')) {
    const u = new URL(line);
    const name = decodeName(u.hash.slice(1));
    return { name, type: 'hysteria2', server: u.hostname, port: parseInt(u.port) || 443, password: u.username };
  }
  if (line.startsWith('vless://')) {
    const u = new URL(line);
    const p = u.searchParams;
    const name = decodeName(u.hash.slice(1));
    const node = {
      name, type: 'vless', server: u.hostname, port: parseInt(u.port),
      uuid: u.username, network: p.get('type') || 'tcp',
      'client-fingerprint': p.get('fp') || 'chrome'
    };
    if (p.get('security') === 'reality') {
      node.tls = true;
      node.servername = p.get('sni') || '';
      node['reality-opts'] = { 'public-key': p.get('pbk'), 'short-id': p.get('sid') || '' };
    }
    if (p.get('flow')) node.flow = p.get('flow');
    return node;
  }
  if (line.startsWith('trojan://')) {
    const u = new URL(line);
    const p = u.searchParams;
    const name = decodeName(u.hash.slice(1));
    const network = p.get('type') || 'tcp';
    const node = { name, type: 'trojan', server: u.hostname, port: parseInt(u.port), password: u.username };
    if (p.get('sni')) node.sni = p.get('sni');
    if (network === 'ws') {
      node.network = 'ws';
      const host = p.get('host') || '';
      if (host) {
        node['ws-opts'] = { path: p.get('path') || '/', headers: { Host: host } };
      }
    }
    return node;
  }
  return null;
}

function nodeToYaml(n) {
  if (n.type === 'hysteria2') {
    return `  - name: "${n.name}"\n    type: hysteria2\n    server: ${n.server}\n    port: ${n.port}\n    password: "${n.password}"`;
  }
  if (n.type === 'vless') {
    let s = `  - name: "${n.name}"\n    type: vless\n    server: ${n.server}\n    port: ${n.port}\n    uuid: ${n.uuid}`;
    if (n['reality-opts']) {
      s += `\n    tls: true\n    servername: ${n.servername}`;
      s += `\n    reality-opts:\n      public-key: ${n['reality-opts']['public-key']}\n      short-id: "${n['reality-opts']['short-id']}"`;
    }
    if (n.flow) s += `\n    flow: ${n.flow}`;
    s += `\n    network: ${n.network}\n    client-fingerprint: ${n['client-fingerprint']}`;
    return s;
  }
  if (n.type === 'trojan') {
    let s = `  - name: "${n.name}"\n    type: trojan\n    server: ${n.server}\n    port: ${n.port}\n    password: "${n.password}"`;
    if (n.sni) s += `\n    sni: ${n.sni}`;
    if (n['ws-opts']) s += `\n    network: ws\n    ws-opts:\n      path: ${n['ws-opts'].path}\n      headers:\n        Host: ${n['ws-opts'].headers.Host}`;
    return s;
  }
  return null;
}

// Main
const subUrl = process.argv[2];
if (subUrl) {
  console.log(`Downloading: ${subUrl}`);
  execSync(`curl -sL '${subUrl}' -o ${SUB_FILE}`);
}

const raw = fs.readFileSync(SUB_FILE, 'utf8').replace(/\s+/g, '').trim();
const decoded = Buffer.from(raw, 'base64').toString('utf8');
const lines = decoded.split('\n').filter(l => l.trim());

const GROUPS = ['日本', '美国', '香港', '台湾', '新加坡', '韩国', '英国', '荷兰', '德国', '其他'];
const regionNodes = {};
GROUPS.forEach(g => regionNodes[g] = []);

const nodes = [];
const seen = new Set();

for (const line of lines) {
  try {
    const node = parseNode(line);
    if (!node || seen.has(node.server + ':' + node.port)) continue;
    seen.add(node.server + ':' + node.port);
    nodes.push(node);

    let matched = false;
    for (const g of GROUPS.slice(0, -1)) {
      if (node.name.includes(g)) { regionNodes[g].push(node.name); matched = true; break; }
    }
    if (!matched) regionNodes['其他'].push(node.name);
  } catch (e) { /* skip */ }
}

console.log(`Parsed ${nodes.length} nodes`);
GROUPS.forEach(g => { if (regionNodes[g].length) console.log(`  ${g}: ${regionNodes[g].length}`); });

const proxiesYaml = nodes.map(nodeToYaml).filter(Boolean).join('\n');

const activeGroups = GROUPS.filter(g => regionNodes[g].length > 0);
const regionGroupsYaml = activeGroups.map(g => {
  const members = regionNodes[g].map(n => `      - "${n}"`).join('\n');
  return `  - name: "${g}"\n    type: select\n    proxies:\n${members}`;
}).join('\n\n');

const config = `mixed-port: 7890
allow-lan: false
mode: rule
log-level: info
external-controller: 127.0.0.1:9090

dns:
  enable: true
  listen: 0.0.0.0:1053
  enhanced-mode: fake-ip
  fake-ip-range: 198.18.0.1/16
  nameserver:
    - 223.5.5.5
    - 119.29.29.29
  fallback:
    - 8.8.8.8
    - 1.1.1.1
  fallback-filter:
    geoip: false
    ipcidr:
      - 240.0.0.0/4

proxies:
${proxiesYaml}

proxy-groups:
  - name: "PROXY"
    type: select
    proxies:
${activeGroups.map(g => `      - "${g}"`).join('\n')}

${regionGroupsYaml}

rules:
  - DOMAIN-SUFFIX,rakuten.co.jp,日本
  - DOMAIN-SUFFIX,amazon.co.jp,日本
  - DOMAIN-SUFFIX,google.com,PROXY
  - DOMAIN-SUFFIX,youtube.com,PROXY
  - DOMAIN-SUFFIX,google.co.jp,日本
  - DOMAIN-SUFFIX,twitter.com,PROXY
  - DOMAIN-SUFFIX,x.com,PROXY
  - DOMAIN-SUFFIX,github.com,PROXY
  - DOMAIN-SUFFIX,openai.com,PROXY
  - DOMAIN-SUFFIX,reddit.com,PROXY
  - DOMAIN-SUFFIX,amazon.com,美国
  - DOMAIN-SUFFIX,netflix.com,美国
  - DOMAIN-SUFFIX,wikipedia.org,PROXY
  - DOMAIN-SUFFIX,telegram.org,PROXY
  - MATCH,DIRECT
`;

fs.writeFileSync(CONFIG_PATH, config);
console.log(`\nConfig written to ${CONFIG_PATH}`);
