/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{js,ts,jsx,tsx}'],
  theme: {
    extend: {
      fontFamily: {
        // Body: Latin first, with Noto Sans SC as the CJK fallback
        body: ['Inter', '"Noto Sans SC"', '"Helvetica Neue"', 'Arial', 'sans-serif'],
        // Display: Latin serif, with a CJK serif fallback for non-Latin output
        display: ['"Playfair Display"', '"Noto Serif SC"', 'serif'],
      },
      colors: {
        // Palette 1 — primary actions, CTAs, highlights
        brand: {
          50: '#FDF6EF',
          100: '#FAE8D6',
          200: '#F3CFA8',
          300: '#E9AE72',
          400: '#DC8B45',
          500: '#C9721F',
          600: '#A85A16',
          700: '#854612',
          800: '#633310',
          900: '#41220B',
        },
        // Palette 2 — success, badges, secondary cues
        fresh: {
          50: '#F2F7EC',
          100: '#E3EFD6',
          200: '#C6DFAC',
          300: '#A3C97C',
          400: '#7FAF52',
          500: '#5F8F38',
          600: '#4A7229',
          700: '#3A5A21',
          800: '#2B4319',
          900: '#1D2E11',
        },
      },
      animation: {
        'fade-in': 'fadeIn 0.5s ease-out',
        'slide-up': 'slideUp 0.5s ease-out',
      },
      keyframes: {
        fadeIn: {
          '0%': { opacity: '0' },
          '100%': { opacity: '1' },
        },
        slideUp: {
          '0%': { opacity: '0', transform: 'translateY(20px)' },
          '100%': { opacity: '1', transform: 'translateY(0)' },
        },
      },
    },
  },
  plugins: [],
};
