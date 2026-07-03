#!/usr/bin/env node
/**
 * Nvidia Shield & Plex Media Server CLI
 * Usage: node shield-cli.js <command> [args]
 */

const { execSync, spawnSync } = require('child_process');
const fs = require('fs');
const path = require('path');
const os = require('os');

const CONFIG_DIR = path.join(os.homedir(), '.openclaw', 'shield');
const CONFIG_FILE = path.join(CONFIG_DIR, 'config.json');

if (!fs.existsSync(CONFIG_DIR)) {
  fs.mkdirSync(CONFIG_DIR, { recursive: true });
}

function loadConfig() {
  if (fs.existsSync(CONFIG_FILE)) {
    return JSON.parse(fs.readFileSync(CONFIG_FILE, 'utf8'));
  }
  return { shield_ip: null, adb_port: 5555, plex_token: null, plex_url: null };
}

function saveConfig(config) {
  fs.writeFileSync(CONFIG_FILE, JSON.stringify(config, null, 2));
  fs.chmodSync(CONFIG_FILE, 0o600);
}

function adb(args) {
  const config = loadConfig();
  const target = `${config.shield_ip}:${config.adb_port}`;
  const result = spawnSync('adb', ['-s', target, ...args], {
    encoding: 'utf8',
    timeout: 15000
  });
  return { stdout: result.stdout?.trim() || '', stderr: result.stderr?.trim() || '', status: result.status };
}

function adbShell(cmd) {
  return adb(['shell', cmd]);
}

function adbConnect() {
  const config = loadConfig();
  const target = `${config.shield_ip}:${config.adb_port}`;
  const result = spawnSync('adb', ['connect', target], { encoding: 'utf8', timeout: 10000 });
  const out = (result.stdout + result.stderr).trim();
  if (out.includes('connected') || out.includes('already connected')) {
    return { connected: true, message: out };
  }
  return { connected: false, message: out };
}

function plexApi(endpoint, method = 'GET', rawXml = false) {
  const config = loadConfig();
  const url = `${config.plex_url}${endpoint}${endpoint.includes('?') ? '&' : '?'}X-Plex-Token=${config.plex_token}`;
  const args = ['-s', '-X', method, url];
  if (!rawXml) {
    args.push('-H', 'Accept: application/json');
  }
  const result = spawnSync('curl', args, { encoding: 'utf8', timeout: 15000 });
  return { stdout: result.stdout?.trim() || '', stderr: result.stderr?.trim() || '', status: result.status };
}

async function main() {
  const command = process.argv[2];
  const args = process.argv.slice(3);

  if (!command) {
    console.error('Usage: node shield-cli.js <command> [args]');
    console.error('\nPlex Commands (no ADB needed):');
    console.error('  discover <plex_token>                            - List all Plex servers on account');
    console.error('  setup <plex_token> [server_index] [shield_ip]    - Auto-discover + configure (default: first server)');
    console.error('  configure <shield_ip> <plex_token> [plex_url]    - Manual config (skip auto-discovery)');
    console.error('  plex-status                                      - Plex server version + platform');
    console.error('  search <query>                                   - Search with full metadata');
    console.error('  format                                           - Format search JSON → readable text');
    console.error('  sessions                                         - Active streams');
    console.error('  libraries                                        - Library sections with IDs');
    console.error('  scan <section_id>                                - Refresh a library');
    console.error('  recently-added                                   - Last 20 additions');
    console.error('  updater-status                                   - Check for Plex updates');
    console.error('  health                                           - Plex status + sessions (+ ADB if configured)');
    console.error('\nShield ADB Commands (require shield_ip):');
    console.error('  connect                                          - ADB connect');
    console.error('  adb-health                                       - Device health (uptime, mem, disk)');
    console.error('  reboot                                           - Reboot Shield');
    console.error('  restart-plex                                     - Force stop + start Plex app');
    process.exit(1);
  }

  if (command === 'discover') {
    if (args.length < 1) {
      console.error('Usage: discover <plex_token>');
      process.exit(1);
    }
    const token = args[0];
    console.error('🔍 Discovering Plex servers...');
    try {
      const discoverResult = spawnSync('curl', [
        '-s', `https://plex.tv/api/resources?X-Plex-Token=${token}`
      ], { encoding: 'utf8', timeout: 15000 });
      const xml = discoverResult.stdout;
      
      // Split by Device blocks to correctly associate connections
      const deviceBlocks = xml.split(/<Device /).slice(1); // skip XML header
      const servers = [];
      
      for (const block of deviceBlocks) {
        // Extract device tag (up to the closing >)
        const tagEnd = block.indexOf('>');
        const tag = '<Device ' + block.slice(0, tagEnd);
        
        // Only interested in owned servers
        if (!/provides="[^"]*server[^"]*"/.test(tag) || !/owned="1"/.test(tag)) continue;
        
        const extract = (attr) => {
          const m = tag.match(new RegExp(attr + '="([^"]*)"'));
          return m ? m[1] : 'unknown';
        };
        
        const server = {
          index: servers.length,
          name: extract('name'),
          product: extract('product'),
          version: extract('productVersion'),
          platform: extract('platform'),
          connections: []
        };
        
        // Extract connections from this device block (up to </Device>)
        const deviceEnd = block.indexOf('</Device>');
        const deviceContent = deviceEnd > 0 ? block.slice(0, deviceEnd) : block;
        const connRegex = /<Connection[^>]*address="([^"]+)"[^>]*port="([^"]+)"[^>]*uri="([^"]+)"[^>]*local="([01])"[^>]*>/g;
        let cm;
        while ((cm = connRegex.exec(deviceContent)) !== null) {
          server.connections.push({
            address: cm[1],
            port: cm[2],
            uri: cm[3],
            local: cm[4] === '1'
          });
        }
        
        const local = server.connections.find(c => c.local);
        server.localUrl = local ? local.uri : (server.connections[0]?.uri || 'unknown');
        servers.push(server);
      }
      
      if (servers.length === 0) {
        console.log(JSON.stringify({ error: 'No Plex servers found on this account.' }));
        process.exit(1);
      }
      
      console.log(JSON.stringify({ count: servers.length, servers }, null, 2));
    } catch (e) {
      console.log(JSON.stringify({ error: e.message }));
      process.exit(1);
    }
    return;
  }

  if (command === 'configure' || command === 'setup') {
    if (args.length < 1) {
      console.error('Usage: setup <plex_token> [server_index] [shield_ip]');
      console.error('  Auto-discovers Plex server via plex.tv API');
      console.error('  server_index: pick a specific server (0 = first, default)');
      console.error('Usage: discover <plex_token>');
      console.error('  List all Plex servers on your account');
      console.error('Usage: configure <shield_ip> <plex_token> [plex_url]');
      console.error('  Manual configuration (skip auto-discovery)');
      process.exit(1);
    }
    
    const config = loadConfig();
    config.plex_token = args[0];
    
    if (command === 'configure') {
      // Manual: user provides IP
      if (args.length < 2) {
        console.error('configure requires: <shield_ip> <plex_token> [plex_url]');
        process.exit(1);
      }
      config.shield_ip = args[1];
      config.plex_url = args[2] || `http://${args[1]}:32400`;
    } else {
      // setup: auto-discover Plex server
      const serverIndex = parseInt(args[1]) || 0;
      const shieldIp = args[1] && isNaN(parseInt(args[1])) ? args[1] : args[2];
      
      console.error('🔍 Discovering Plex servers...');
      try {
        const discoverResult = spawnSync('curl', [
          '-s', `https://plex.tv/api/resources?X-Plex-Token=${config.plex_token}`
        ], { encoding: 'utf8', timeout: 15000 });
        
        const xml = discoverResult.stdout;
        
        // Find all owned server devices
        const serverRegex = /<Device[^>]*name="([^"]+)"[^>]*provides="[^"]*server[^"]*"[^>]*owned="1"[^>]*>/g;
        const servers = [];
        let match;
        while ((match = serverRegex.exec(xml)) !== null) {
          const tag = match[0];
          const extract = (attr) => {
            const m = tag.match(new RegExp(attr + '="([^"]*)"'));
            return m ? m[1] : 'unknown';
          };
          servers.push({
            name: match[1],
            product: extract('product'),
            version: extract('productVersion'),
            platform: extract('platform')
          });
        }
        
        if (servers.length === 0) {
          console.error('❌ No Plex servers found on your account.');
          process.exit(1);
        }
        
        if (serverIndex >= servers.length) {
          console.error(`❌ Server index ${serverIndex} out of range. Found ${servers.length} server(s).`);
          console.error('Run: node shield-cli.js discover <token> to see all servers.');
          process.exit(1);
        }
        
        const chosen = servers[serverIndex];
        
        // Find local connection for the chosen server
        // Strategy: find the N-th occurrence of local connection on port 32400
        const allLocalConns = [...xml.matchAll(/<Connection[^>]*address="([^"]+)"[^>]*port="32400"[^>]*local="1"[^>]*>/g)];
        let localUrl;
        if (allLocalConns[serverIndex]) {
          localUrl = `http://${allLocalConns[serverIndex][1]}:32400`;
          config.shield_ip = allLocalConns[serverIndex][1];
        } else {
          // Fallback: any local connection
          const anyLocal = [...xml.matchAll(/<Connection[^>]*address="([^"]+)"[^>]*port="([^"]+)"[^>]*local="1"[^>]*>/g)];
          if (anyLocal[serverIndex]) {
            localUrl = `http://${anyLocal[serverIndex][1]}:${anyLocal[serverIndex][2]}`;
            config.shield_ip = anyLocal[serverIndex][1];
          } else if (anyLocal[0]) {
            localUrl = `http://${anyLocal[0][1]}:${anyLocal[0][2]}`;
            config.shield_ip = anyLocal[0][1];
          } else {
            console.error('❌ Could not determine local IP. Use configure instead.');
            process.exit(1);
          }
        }
        config.plex_url = localUrl;
        
        if (servers.length > 1) {
          console.error(`✅ Selected server ${serverIndex}: "${chosen.name}" (${chosen.platform}) at ${config.plex_url}`);
        } else {
          console.error(`✅ Found "${chosen.name}" (${chosen.platform}) at ${config.plex_url}`);
        }
        
        // Optional Shield IP for ADB
        if (shieldIp) {
          config.shield_ip = shieldIp;
          console.error(`📱 Shield ADB target: ${shieldIp}:${config.adb_port}`);
        }
      } catch (e) {
        console.error(`❌ Auto-discovery failed: ${e.message}`);
        console.error('Use configure <shield_ip> <plex_token> for manual setup.');
        process.exit(1);
      }
    }
    
    saveConfig(config);
    console.log(JSON.stringify({ status: 'configured', plex_url: config.plex_url, shield_ip: config.shield_ip, plex_token: '***' }, null, 2));
    return;
  }

  const config = loadConfig();
  if (!config.plex_token) {
    console.error('Error: Not configured. Run: node shield-cli.js setup <plex_token>');
    process.exit(1);
  }
  
  // Commands that need ADB
  const adbCommands = ['connect', 'adb-health', 'reboot', 'restart-plex'];
  if (adbCommands.includes(command) && !config.shield_ip) {
    console.error('Error: Shield IP not configured. Run: node shield-cli.js setup <plex_token> <shield_ip>');
    process.exit(1);
  }

  try {
    switch (command) {
      case 'connect': {
        const result = adbConnect();
        console.log(JSON.stringify(result, null, 2));
        break;
      }

      case 'health': {
        const output = {};

        // ADB health
        const conn = adbConnect();
        output.adb_connected = conn.connected;
        output.adb_message = conn.message;

        if (conn.connected) {
          const uptime = adbShell('uptime');
          output.uptime = uptime.stdout;

          const mem = adbShell('dumpsys meminfo | grep "Used RAM"');
          output.memory = mem.stdout;

          const disk = adbShell('df -h /data /sdcard 2>/dev/null');
          output.disk = disk.stdout;

          const plexProc = adbShell('ps -A | grep -i plex');
          output.plex_process = plexProc.stdout || 'NOT RUNNING';

          const battery = adbShell('dumpsys battery | grep -E "level|temperature|status"');
          output.battery = battery.stdout;
        }

        // Plex health
        const plexStatus = plexApi('/');
        try {
          const status = JSON.parse(plexStatus.stdout);
          output.plex = {
            friendlyName: status.MediaContainer?.friendlyName,
            version: status.MediaContainer?.version,
            platform: status.MediaContainer?.platform,
            size: status.MediaContainer?.size
          };
        } catch (_) {
          output.plex = { error: 'Could not reach Plex', raw: plexStatus.stdout?.slice(0, 200) };
        }

        // Plex sessions
        const sessions = plexApi('/status/sessions');
        try {
          const sess = JSON.parse(sessions.stdout);
          output.active_sessions = (sess.MediaContainer?.Metadata || []).map(s => ({
            title: s.title,
            type: s.type,
            user: s.User?.title,
            player: s.Player?.title,
            state: s.Player?.state,
            progress: s.viewOffset ? `${Math.round(s.viewOffset / 60000)}min / ${Math.round(s.duration / 60000)}min` : 'N/A'
          }));
        } catch (_) {
          output.active_sessions = [];
        }

        console.log(JSON.stringify(output, null, 2));
        break;
      }

      case 'adb-health': {
        const conn = adbConnect();
        if (!conn.connected) {
          console.log(JSON.stringify({ error: 'ADB not connected', message: conn.message }));
          process.exit(1);
        }

        const output = {};
        output.uptime = adbShell('uptime').stdout;
        output.memory = adbShell('dumpsys meminfo | grep "Used RAM"').stdout;
        output.disk = adbShell('df -h /data /sdcard 2>/dev/null').stdout;
        output.plex_process = adbShell('ps -A | grep -i plex').stdout || 'NOT RUNNING';
        output.battery = adbShell('dumpsys battery | grep -E "level|temperature|status"').stdout;
        console.log(JSON.stringify(output, null, 2));
        break;
      }

      case 'plex-status': {
        const result = plexApi('/');
        try {
          const status = JSON.parse(result.stdout);
          console.log(JSON.stringify({
            friendlyName: status.MediaContainer?.friendlyName,
            version: status.MediaContainer?.version,
            platform: status.MediaContainer?.platform,
            machineIdentifier: status.MediaContainer?.machineIdentifier,
            size: status.MediaContainer?.size
          }, null, 2));
        } catch (_) {
          console.log(JSON.stringify({ error: 'Could not parse Plex response', raw: result.stdout?.slice(0, 300) }));
        }
        break;
      }

      case 'sessions': {
        const result = plexApi('/status/sessions');
        try {
          const data = JSON.parse(result.stdout);
          const sessions = (data.MediaContainer?.Metadata || []).map(s => ({
            title: s.title,
            grandparentTitle: s.grandparentTitle || null,
            type: s.type,
            user: s.User?.title,
            player: s.Player?.title,
            device: s.Player?.device,
            state: s.Player?.state,
            progress: s.viewOffset ? `${Math.round(s.viewOffset / 60000)}min / ${Math.round(s.duration / 60000)}min` : 'N/A',
            transcoding: s.TranscodeSession ? {
              videoDecision: s.TranscodeSession?.videoDecision,
              audioDecision: s.TranscodeSession?.audioDecision
            } : null
          }));
          console.log(JSON.stringify({ count: sessions.length, sessions }, null, 2));
        } catch (_) {
          console.log(JSON.stringify({ count: 0, sessions: [] }));
        }
        break;
      }

      case 'libraries': {
        const result = plexApi('/library/sections');
        try {
          const data = JSON.parse(result.stdout);
          const libs = (data.MediaContainer?.Directory || []).map(d => ({
            key: d.key,
            title: d.title,
            type: d.type,
            path: d.Location?.map(l => l.path)
          }));
          console.log(JSON.stringify(libs, null, 2));
        } catch (_) {
          console.log(JSON.stringify({ error: 'Could not fetch libraries' }));
        }
        break;
      }

      case 'search': {
        const query = args.join(' ');
        if (!query) {
          console.error('Usage: search <query>');
          process.exit(1);
        }
        const result = plexApi(`/search?query=${encodeURIComponent(query)}`);
        try {
          const data = JSON.parse(result.stdout);
          const items = data.MediaContainer?.Metadata || [];
          
          // Fetch full metadata for each local result to get quality, audio, etc.
          const results = [];
          for (const r of items) {
            const isLocal = !!r.librarySectionTitle;
            const base = {
              title: r.title,
              type: r.type,
              year: r.year,
              source: isLocal ? 'local' : 'streaming',
              libraryTitle: r.librarySectionTitle || 'Plex Online / Streaming',
              summary: r.summary?.slice(0, 200)
            };
            
            // Get detailed metadata for local items
            if (isLocal && r.ratingKey) {
              try {
                const metaResult = plexApi(`/library/metadata/${r.ratingKey}`);
                const meta = JSON.parse(metaResult.stdout);
                const m = meta.MediaContainer?.Metadata?.[0];
                if (m) {
                  base.duration = m.duration ? `${Math.round(m.duration / 60000)} min` : null;
                  base.studio = m.studio;
                  base.contentRating = m.contentRating;
                  base.rating = m.rating;
                  base.originallyAvailableAt = m.originallyAvailableAt;
                  base.viewCount = m.viewCount;
                  if (m.Genre?.length) {
                    base.genres = m.Genre.map(g => g.tag);
                  }
                  if (m.Media?.length) {
                    base.media = m.Media.map(med => ({
                      resolution: med.videoResolution,
                      width: med.width,
                      height: med.height,
                      videoCodec: med.videoCodec,
                      audioCodec: med.audioCodec,
                      audioChannels: med.audioChannels,
                      container: med.container,
                      bitrate: med.bitrate ? `${Math.round(med.bitrate / 1000)} Mbps` : null,
                      file: med.Part?.[0]?.file?.split('/').pop() || null,
                      size: med.Part?.[0]?.size ? `${(med.Part[0].size / 1024 / 1024 / 1024).toFixed(1)} GB` : null
                    }));
                  }
                  
                  // Fetch XML for stream details (languages)
                  try {
                    const xmlResult = plexApi(`/library/metadata/${r.ratingKey}`, 'GET', true);
                    const xml = xmlResult.stdout;
                    const streamRegex = /<Stream[^>]*streamType="(\d+)"[^>]*codec="([^"]+)"[^>]*language="([^"]+)"[^>]*displayTitle="([^"]*)"[^>]*>/g;
                    let smatch;
                    const streams = { audio: [], subtitles: [] };
                    while ((smatch = streamRegex.exec(xml)) !== null) {
                      if (smatch[1] === '2') {
                        streams.audio.push({ codec: smatch[2], language: smatch[3], displayTitle: smatch[4] });
                      } else if (smatch[1] === '3') {
                        streams.subtitles.push({ codec: smatch[2], language: smatch[3], displayTitle: smatch[4] });
                      }
                    }
                    if (streams.audio.length) base.audioLanguages = streams.audio;
                    if (streams.subtitles.length) base.subtitleLanguages = streams.subtitles;
                  } catch (_) { /* skip stream details */ }
                }
              } catch (_) { /* skip metadata enrichment */ }
            }
            results.push(base);
          }
          console.log(JSON.stringify({ query, count: results.length, results }, null, 2));
        } catch (_) {
          console.log(JSON.stringify({ query, count: 0, results: [] }));
        }
        break;
      }

      case 'scan': {
        const sectionId = args[0];
        if (!sectionId) {
          console.error('Usage: scan <section_id>');
          process.exit(1);
        }
        const result = plexApi(`/library/sections/${sectionId}/refresh`, 'PUT');
        console.log(JSON.stringify({ status: 'scan_started', section_id: sectionId, response: result.status }));
        break;
      }

      case 'recently-added': {
        const result = plexApi('/library/recentlyAdded');
        try {
          const data = JSON.parse(result.stdout);
          const items = (data.MediaContainer?.Metadata || []).slice(0, 20).map(r => ({
            title: r.title,
            type: r.type,
            year: r.year,
            addedAt: new Date(r.addedAt * 1000).toISOString().split('T')[0],
            libraryTitle: r.librarySectionTitle
          }));
          console.log(JSON.stringify({ count: items.length, items }, null, 2));
        } catch (_) {
          console.log(JSON.stringify({ count: 0, items: [] }));
        }
        break;
      }

      case 'updater-status': {
        const result = plexApi('/updater/status');
        console.log(result.stdout || JSON.stringify({ status: 'no_update_info' }));
        break;
      }

      case 'reboot': {
        const conn = adbConnect();
        if (!conn.connected) {
          console.log(JSON.stringify({ error: 'ADB not connected', message: conn.message }));
          process.exit(1);
        }
        console.log(JSON.stringify({ status: 'rebooting' }));
        adb(['reboot']);
        break;
      }

      case 'restart-plex': {
        const conn = adbConnect();
        if (!conn.connected) {
          console.log(JSON.stringify({ error: 'ADB not connected', message: conn.message }));
          process.exit(1);
        }
        adbShell('am force-stop com.plexapp.mediaserver.smb');
        console.log(JSON.stringify({ status: 'plex_stopped' }));
        // Give it a moment, then start
        await new Promise(r => setTimeout(r, 2000));
        adbShell('am start -n com.plexapp.mediaserver.smb/.MainActivity');
        console.log(JSON.stringify({ status: 'plex_restarted' }));
        break;
      }

      case 'format': {
        // Read JSON from stdin and produce human-readable output
        const chunks = [];
        process.stdin.setEncoding('utf8');
        for await (const chunk of process.stdin) {
          chunks.push(chunk);
        }
        const input = JSON.parse(chunks.join(''));
        const lines = [];
        
        const emoji = { movie: '🎬', show: '📺', artist: '🎵', album: '💿', track: '🎧' };
        const resEmoji = { '4k': '📺', '1080': '🖥️', '720': '💻', '480': '📱', 'sd': '📱' };
        
        const query = input.query || '';
        const results = input.results || [];
        const localResults = results.filter(r => r.source === 'local');
        const streamingResults = results.filter(r => r.source === 'streaming');
        
        if (results.length === 0) {
          lines.push(`🔍 **${query}** — nessun risultato trovato.`);
        } else {
          const icon = emoji[results[0]?.type] || '🎞️';
          lines.push(`${icon} **${query}** — ${results.length} risultato${results.length !== 1 ? 'i' : ''} trovato${results.length !== 1 ? 'i' : ''}`);
          lines.push('');
        }
        
        for (const r of results) {
          const typeLabel = r.type === 'movie' ? 'Film' : r.type === 'show' ? 'Serie TV' : r.type;
          const sourceLabel = r.source === 'local' ? `📁 ${r.libraryTitle}` : '🌐 Plex Online';
          
          lines.push(`**${r.title}** (${r.year || '?'})`);
          lines.push(`- 🎞️ ${typeLabel} · ${sourceLabel}`);
          
          const details = [];
          if (r.duration) details.push(`⏱️ ${r.duration}`);
          if (r.genres?.length) details.push(`🏷️ ${r.genres.join(', ')}`);
          if (r.studio) details.push(`🏢 ${r.studio}`);
          if (r.contentRating) details.push(`🎬 ${r.contentRating}`);
          if (details.length) lines.push(`- ${details.join(' · ')}`);
          
          const ratings = [];
          if (r.rating) ratings.push(`⭐ ${r.rating}`);
          if (r.viewCount > 0) ratings.push(`👁️ Visto ${r.viewCount} volt${r.viewCount !== 1 ? 'e' : 'a'}`);
          if (ratings.length) lines.push(`- ${ratings.join(' · ')}`);
          
          if (r.media?.length) {
            for (const med of r.media) {
              const qual = [];
              if (med.resolution) qual.push(`${resEmoji[med.resolution] || '📺'} ${med.resolution.toUpperCase()}`);
              if (med.width && med.height) qual.push(`${med.width}×${med.height}`);
              if (med.videoCodec) qual.push(med.videoCodec.toUpperCase());
              if (med.bitrate) qual.push(med.bitrate);
              if (med.container) qual.push(med.container.toUpperCase());
              if (med.size) qual.push(med.size);
              lines.push(`- **📺 Qualità:** ${qual.join(' · ')}`);
            }
          }
          
          if (r.audioLanguages?.length) {
            const audio = r.audioLanguages.map(a => a.displayTitle || `${a.language} (${a.codec})`);
            lines.push(`- **🔊 Audio:** ${audio.join(' · ')}`);
          }
          
          if (r.subtitleLanguages?.length) {
            const subs = r.subtitleLanguages.map(s => {
              const title = (s.displayTitle || s.language)
                .replace(/&#241;/g, 'ñ')
                .replace(/&#231;/g, 'ç')
                .replace(/&#233;/g, 'é')
                .replace(/&#224;/g, 'à')
                .replace(/&#232;/g, 'è')
                .replace(/&#242;/g, 'ò')
                .replace(/&#249;/g, 'ù')
                .replace(/&#243;/g, 'ó')
                .replace(/&#237;/g, 'í')
                .replace(/&#225;/g, 'á')
                .replace(/&#250;/g, 'ú');
              return title;
            });
            const uniqueSubs = [...new Set(subs)];
            lines.push(`- **💬 Sottotitoli:** ${uniqueSubs.join(' · ')}`);
          }
          
          if (r.summary) {
            lines.push(`- 📝 ${r.summary}`);
          }
          
          lines.push('');
        }
        
        // Streaming results summary
        if (streamingResults.length > 0) {
          lines.push(`🌐 **Disponibile in streaming:** ${streamingResults.map(r => r.title).join(', ')}`);
          lines.push('');
        }
        
        console.log(lines.join('\n'));
        break;
      }

      default:
        console.error(`Unknown command: ${command}`);
        process.exit(1);
    }
  } catch (e) {
    console.error(`Error: ${e.message}`);
    process.exit(1);
  }
}

main().catch(err => {
  console.error(err);
  process.exit(1);
});
