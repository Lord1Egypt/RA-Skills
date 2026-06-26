import { useEffect, useState } from 'react';

type GuildEntry = { id: string; name?: string };

export function App() {
  const [guildId, setGuildId] = useState('');
  const [guilds, setGuilds] = useState<GuildEntry[]>([]);
  const [settingsJson, setSettingsJson] = useState('{\n  "ticketCategoryId": "",\n  "staffRoleId": ""\n}');
  const [status, setStatus] = useState('idle');

  async function loadGuilds() {
    setStatus('loading guilds');
    const res = await fetch('/dashboard/guilds', { credentials: 'include' });
    if (!res.ok) {
      setStatus('guild load failed');
      return;
    }
    const data = await res.json();
    setGuilds(data);
    setStatus('guilds loaded');
  }

  async function loadSettings(targetGuildId: string) {
    setStatus('loading');
    const res = await fetch(`/dashboard/guilds/${targetGuildId}/settings`, { credentials: 'include' });
    const data = await res.json();
    setGuildId(targetGuildId);
    setSettingsJson(JSON.stringify(data.settings ?? {}, null, 2));
    setStatus('loaded');
  }

  async function saveSettings() {
    setStatus('saving');
    await fetch(`/dashboard/guilds/${guildId}/settings`, {
      method: 'PUT',
      credentials: 'include',
      headers: { 'Content-Type': 'application/json' },
      body: settingsJson
    });
    setStatus('saved');
  }

  async function logout() {
    await fetch('/auth/logout', { method: 'POST', credentials: 'include' });
    setGuilds([]);
    setGuildId('');
    setStatus('logged out');
  }

  useEffect(() => {
    loadGuilds().catch(() => setStatus('guild load failed'));
  }, []);

  return (
    <main style={{ fontFamily: 'sans-serif', padding: 24, maxWidth: 1100, margin: '0 auto', display: 'grid', gridTemplateColumns: '280px 1fr', gap: 24 }}>
      <aside>
        <h2>Guilds</h2>
        <p><a href="/auth/discord">Login with Discord</a></p>
        <button onClick={loadGuilds}>Refresh Guilds</button>
        <button onClick={logout} style={{ marginLeft: 8 }}>Logout</button>
        <ul>
          {guilds.map((guild) => (
            <li key={guild.id}>
              <button onClick={() => loadSettings(guild.id)}>{guild.name || guild.id}</button>
            </li>
          ))}
        </ul>
      </aside>
      <section>
        <h1>Discord Dashboard Starter</h1>
        <p>Selected guild: {guildId || 'none'}</p>
        <textarea value={settingsJson} onChange={(e) => setSettingsJson(e.target.value)} rows={22} style={{ width: '100%', fontFamily: 'monospace' }} />
        <div style={{ marginTop: 16, display: 'flex', gap: 12 }}>
          <button onClick={saveSettings} disabled={!guildId}>Save</button>
        </div>
        <p>Status: {status}</p>
      </section>
    </main>
  );
}
