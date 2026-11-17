export function canUseDemo(screens) {
  return Array.isArray(screens) && screens.some((screen) => screen.entry === true)
}
