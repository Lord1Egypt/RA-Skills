const ScreenIdentityContext = React.createContext(null)

export function ScreenIdentityProvider({ screenId, children }) {
  if (!screenId) throw new Error('ScreenIdentityProvider requires screenId')
  return (
    <ScreenIdentityContext.Provider value={screenId}>
      {children}
    </ScreenIdentityContext.Provider>
  )
}

export function useScreenId() {
  const screenId = React.useContext(ScreenIdentityContext)
  if (!screenId) {
    throw new Error('useScreenId must be used inside a rendered screen')
  }
  return screenId
}
