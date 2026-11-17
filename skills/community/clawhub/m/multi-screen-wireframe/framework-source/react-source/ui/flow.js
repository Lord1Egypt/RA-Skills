import { usePrototype } from '../core/PrototypeContext.jsx'

export { findFlowTargetId, handleDelegatedFlowClick } from './flow-target.js'

export function createFlowProps(to, onClick, navigate) {
  return {
    'data-flow-to': to || undefined,
    onClick: (event) => {
      if (to) event.stopPropagation?.()
      if (onClick) onClick(event)
      if (!event.defaultPrevented && to) navigate(to)
    },
  }
}

export function useFlowTarget(to, onClick) {
  const { navigate } = usePrototype()
  return createFlowProps(to, onClick, navigate)
}
