/**
 * 热区与跳转的唯一契约：元素带 data-flow-to 即可导航。
 * ScreenFrame 委托点击兜底，避免业务写成裸 span/div 只有属性、没有 onClick。
 */
export function findFlowTargetId(startEl, rootEl) {
  if (!startEl || typeof startEl.closest !== 'function') return null
  const el = startEl.closest('[data-flow-to]')
  if (!el) return null
  if (rootEl && typeof rootEl.contains === 'function' && !rootEl.contains(el)) return null
  const to = el.getAttribute('data-flow-to')
  return to || null
}

export function handleDelegatedFlowClick(event, rootEl, navigate) {
  const to = findFlowTargetId(event?.target, rootEl)
  if (!to) return false
  event.preventDefault?.()
  event.stopPropagation?.()
  navigate(to)
  return true
}
