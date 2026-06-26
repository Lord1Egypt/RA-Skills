export default function Tag({ children, type = 'gray', style }) {
  return (
    <span className={`tag ${type}`} style={style}>
      {children}
    </span>
  )
}
