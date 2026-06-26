/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{js,jsx}'],
  theme: {
    extend: {
      colors: {
        oc: {
          bg:      '#0a0a0a',
          surface: '#141414',
          s2:      '#1c1c1c',
          s3:      '#242424',
          border:  '#2e2e2e',
          muted:   '#606060',
          text:    '#e0e0e0',
        },
      },
      fontFamily: {
        mono: ["'SF Mono'", "'Fira Code'", "'Cascadia Code'", 'monospace'],
      },
    },
  },
  plugins: [],
}
