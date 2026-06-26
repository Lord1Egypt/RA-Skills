'use client'

/**
 * TerminalSteps — animated dark terminal window
 *
 * Use in the **Agitate** section of your landing page.
 * Show the painful, tedious steps your customer has to take WITHOUT your product.
 * The goal: make them feel the friction before you offer the escape.
 *
 * Usage:
 *   <TerminalSteps steps={mySteps} title="~/the-old-way — bash" />
 *
 * Or use the default placeholder steps and edit them in place.
 */

import { motion } from 'framer-motion'

interface Step {
  n: string
  text: string
}

interface TerminalStepsProps {
  steps?: Step[]
  /**
   * Text shown in the terminal title bar.
   * Convention: '~/description-of-hard-way — bash'
   */
  title?: string
}

const DEFAULT_STEPS: Step[] = [
  { n: '01', text: 'Research your options. Compare twelve competing tools. Read docs. Set up trial accounts.' },
  { n: '02', text: 'Configure the integrations manually. Debug auth errors. Write the custom glue code.' },
  { n: '03', text: 'Deploy to staging. Hit incompatibilities. Roll back. Patch. Redeploy. Repeat.' },
  { n: '04', text: 'Onboard your team. Re-explain the setup every time someone touches the config.' },
  { n: '05', text: 'Maintain it. Patch it when dependencies update. When it breaks at 3am — you wake up.' },
]

const container = {
  hidden: {},
  show: {
    transition: { staggerChildren: 0.22, delayChildren: 0.1 },
  },
}

const item = {
  hidden: { opacity: 0, x: -12 },
  show: {
    opacity: 1,
    x: 0,
    transition: { duration: 0.45, ease: [0.16, 1, 0.3, 1] as [number, number, number, number] },
  },
}

export function TerminalSteps({
  steps = DEFAULT_STEPS,
  title = '~/the-old-way — bash',
}: TerminalStepsProps) {
  return (
    <motion.div
      className="rounded-xl overflow-hidden border border-zinc-800/80"
      style={{ background: '#080810' }}
      initial={{ opacity: 0, y: 20 }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true, margin: '-80px' }}
      transition={{ duration: 0.6, ease: [0.16, 1, 0.3, 1] }}
    >
      {/* Terminal title bar */}
      <div
        className="px-4 py-3 border-b border-zinc-800/60 flex items-center gap-2"
        style={{ background: '#0c0c16' }}
      >
        <div className="flex gap-1.5">
          <div className="w-3 h-3 rounded-full bg-red-500/70" />
          <div className="w-3 h-3 rounded-full bg-yellow-500/70" />
          <div className="w-3 h-3 rounded-full bg-green-500/70" />
        </div>
        <span className="text-zinc-500 text-xs font-mono ml-3">{title}</span>
      </div>

      {/* Steps */}
      <div className="p-5 space-y-4">
        <motion.div
          variants={container}
          initial="hidden"
          whileInView="show"
          viewport={{ once: true }}
        >
          {steps.map((step) => (
            <motion.div key={step.n} variants={item} className="flex gap-3 items-start mb-3 last:mb-0">
              <span className="text-amber-500/50 shrink-0 text-xs font-mono mt-0.5 w-5">{step.n}</span>
              <p className="text-zinc-400/65 leading-relaxed text-[13px] font-mono">{step.text}</p>
            </motion.div>
          ))}

          {/* Blinking cursor */}
          <motion.div
            variants={item}
            className="flex items-center gap-2 text-zinc-600 font-mono text-sm mt-2"
          >
            <span className="text-amber-500/30">$</span>
            <span className="inline-block w-2 h-[14px] bg-zinc-600/60 cursor-blink" />
          </motion.div>
        </motion.div>
      </div>
    </motion.div>
  )
}
