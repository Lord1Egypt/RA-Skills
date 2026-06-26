export default function ProgressBar({ percent, warning = false }) {
  const bgStyle = warning 
    ? { background: 'linear-gradient(90deg, #f7c03e, #e19a2d)' }
    : { background: 'linear-gradient(90deg, #7babff, #4b87f8)' }

  return (
    <div className="progress-bar">
      <span style={{ width: `${percent}%`, ...bgStyle }}></span>
    </div>
  )
}
