export default function NoteItem({ title, content, priority = 'low' }) {
  const dotClass = priority === 'high' ? 'dot-high' : priority === 'mid' ? 'dot-mid' : 'dot-low'
  const borderColor = priority === 'high' ? '#ef5f59' : priority === 'mid' ? '#f7c03e' : '#46bc46'

  return (
    <div className="note-item" style={{ borderLeft: `3px solid ${borderColor}` }}>
      <div className="list-item-title">
        <span className={`priority-dot ${dotClass}`}></span>
        {title}
      </div>
      <p className="muted-text">{content}</p>
    </div>
  )
}
