// Add these to your tailwind.config.js
// Merge into the existing `theme: { extend: { ... } }` block

module.exports = {
  theme: {
    extend: {
      fontFamily: {
        display: ['var(--font-display)', 'sans-serif'],
        sans:    ['var(--font-sans)',    'sans-serif'],
        mono:    ['var(--font-mono)',    'monospace'],
      },
      colors: {
        // Replace all values below with your brand color
        brand: {
          DEFAULT: '#f97316',  // your primary CTA color
          light:   '#fb923c',  // lighter tint (hover states, text)
          dark:    '#ea580c',  // darker shade (pressed states)
          glow:    'rgba(249,115,22,0.3)',  // low-opacity for box-shadow glow
        },
      },
      animation: {
        'fade-up':       'fade-up 0.6s ease both',
        'logo-breathe':  'logo-breathe 3.5s ease-in-out infinite',
        'pulse-glow':    'pulse-glow 2.5s ease-in-out infinite',
      },
      keyframes: {
        'fade-up': {
          '0%':   { opacity: '0', transform: 'translateY(20px)' },
          '100%': { opacity: '1', transform: 'translateY(0)'    },
        },
        'logo-breathe': {
          '0%,100%': { transform: 'scale(1)'    },
          '50%':     { transform: 'scale(1.06)' },
        },
        // Replace rgba values with your brand accent color
        'pulse-glow': {
          '0%,100%': { boxShadow: '0 0 20px rgba(var(--brand-rgb), 0.3)' },
          '50%':     { boxShadow: '0 0 35px rgba(var(--brand-rgb), 0.55)' },
        },
      },
    },
  },
}
