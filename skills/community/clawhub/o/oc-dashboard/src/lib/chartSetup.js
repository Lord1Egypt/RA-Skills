import {
  Chart as ChartJS,
  CategoryScale, LinearScale,
  PointElement, LineElement,
  BarElement, BarController,
  Filler, Tooltip, Legend,
} from 'chart.js'

ChartJS.register(
  CategoryScale, LinearScale,
  PointElement, LineElement,
  BarElement, BarController,
  Filler, Tooltip, Legend,
)

// Global dark-theme defaults
ChartJS.defaults.color = '#606060'
ChartJS.defaults.borderColor = '#1c1c1c'
ChartJS.defaults.font.family = "'SF Mono', 'Fira Code', monospace"
ChartJS.defaults.font.size = 10
