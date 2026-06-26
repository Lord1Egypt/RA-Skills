const THEMES = {
  aurora: {
    name: 'aurora',
    background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
    header: 'linear-gradient(135deg, #11998e 0%, #38ef7d 100%)',
    accent: '#667eea',
    textPrimary: '#1f2937',
    textSecondary: '#4b5563',
    card: '#ffffff'
  },
  sunset: {
    name: 'sunset',
    background: 'linear-gradient(135deg, #ff7e5f 0%, #feb47b 100%)',
    header: 'linear-gradient(135deg, #f83600 0%, #f9d423 100%)',
    accent: '#ff7e5f',
    textPrimary: '#1f1f1f',
    textSecondary: '#4a4a4a',
    card: '#ffffff'
  },
  midnight: {
    name: 'midnight',
    background: 'linear-gradient(135deg, #0f172a 0%, #1e293b 100%)',
    header: 'linear-gradient(135deg, #2563eb 0%, #10b981 100%)',
    accent: '#38bdf8',
    textPrimary: '#e5e7eb',
    textSecondary: '#cbd5e1',
    card: 'rgba(15, 23, 42, 0.8)'
  },
  ocean: {
    name: 'ocean',
    background: 'linear-gradient(135deg, #1e3c72 0%, #2a5298 100%)',
    header: 'linear-gradient(135deg, #0f9b8e 0%, #00b4db 100%)',
    accent: '#00b4db',
    textPrimary: '#0f172a',
    textSecondary: '#1f2937',
    card: '#f5f7fb'
  },
  forest: {
    name: 'forest',
    background: 'linear-gradient(135deg, #134e5e 0%, #71b280 100%)',
    header: 'linear-gradient(135deg, #2e8b57 0%, #56ab2f 100%)',
    accent: '#4caf50',
    textPrimary: '#102a27',
    textSecondary: '#305f4d',
    card: '#f5f7f2'
  },
  mono: {
    name: 'mono',
    background: 'linear-gradient(135deg, #2c3e50 0%, #bdc3c7 100%)',
    header: 'linear-gradient(135deg, #4b5563 0%, #9ca3af 100%)',
    accent: '#111827',
    textPrimary: '#111827',
    textSecondary: '#4b5563',
    card: '#ffffff'
  }
};

function resolveTheme(themeName, accent) {
  const base = THEMES[themeName] || THEMES.aurora;
  return {
    ...base,
    accent: accent || base.accent
  };
}

module.exports = {
  THEMES,
  resolveTheme
};
