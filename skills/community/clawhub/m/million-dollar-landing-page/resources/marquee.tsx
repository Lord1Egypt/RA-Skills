/**
 * Marquee — infinite horizontal scroll strip
 *
 * Use for: platform names, client logos, integrations, feature names,
 * social proof snippets — anything that benefits from a "wall of proof".
 *
 * Usage:
 *   <Marquee items={['Stripe', 'Shopify', 'HubSpot', 'Notion']} />
 *
 * Customise:
 *   - items: string[] — the list to scroll (automatically doubled for seamless loop)
 *   - bgColor: match your page background so the fade-edge gradient blends correctly
 *   - separatorColor: Tailwind class for the dot separator between items
 */

interface MarqueeProps {
  items: string[]
  /**
   * Must match your page background color exactly for the fade edges to work.
   * e.g. '#050810', '#0a0a0a', '#ffffff'
   */
  bgColor?: string
  /**
   * Tailwind color class for the separator dot between items.
   * e.g. 'text-white/20', 'text-indigo-500/20'
   */
  separatorColor?: string
}

export function Marquee({
  items,
  bgColor = '#050810',
  separatorColor = 'text-white/20',
}: MarqueeProps) {
  const doubled = [...items, ...items]

  return (
    <div className="relative overflow-hidden py-1">
      {/* Fade edges — must match page background */}
      <div
        className="absolute left-0 inset-y-0 w-16 z-10 pointer-events-none"
        style={{ background: `linear-gradient(to right, ${bgColor}, transparent)` }}
      />
      <div
        className="absolute right-0 inset-y-0 w-16 z-10 pointer-events-none"
        style={{ background: `linear-gradient(to left, ${bgColor}, transparent)` }}
      />

      <div className="marquee-track">
        {doubled.map((item, i) => (
          <span
            key={i}
            className="inline-flex items-center gap-3 px-4 text-sm font-medium text-white/25 whitespace-nowrap"
          >
            {item}
            <span className={separatorColor}>·</span>
          </span>
        ))}
      </div>
    </div>
  )
}
