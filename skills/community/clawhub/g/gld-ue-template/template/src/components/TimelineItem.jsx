export default function TimelineItem({ title, meta, tag }) {
  return (
    <div className="timeline-item">
      <div className="timeline-title">{title}</div>
      <div className="timeline-meta">
        {meta} {tag}
      </div>
    </div>
  )
}
