---
name: senior-frontend
description: Build, optimize, and review React and Next.js applications with TypeScript and Tailwind CSS. Use when scaffolding a frontend project, generating components, analyzing bundle size, optimizing Next.js performance (Server Components, image loading, data fetching), implementing accessibility, or reviewing frontend code quality.
compatibility: Requires Python 3.8+ for scripts in scripts/.
---

# Senior Frontend

React, Next.js, TypeScript, and Tailwind CSS — from scaffold to production.

## Activation

Use this skill when the user asks to:
- scaffold a new Next.js or React + Vite project
- generate a React component, custom hook, or Storybook story
- analyze or reduce bundle size
- optimize Next.js (Server vs Client Components, image loading, data fetching)
- implement accessibility (WCAG, ARIA, keyboard navigation)
- review or improve frontend code quality

## Workflow

1. **Classify** the request: `scaffold` | `component` | `bundle` | `optimize` | `accessibility` | `review`.
2. **Load the relevant reference**:
   - React patterns (compound components, custom hooks, render props) → `{baseDir}/references/react_patterns.md`
   - Next.js optimization (Server Components, Suspense, images, caching) → `{baseDir}/references/nextjs_optimization_guide.md`
   - accessibility, testing strategy, Tailwind conventions → `{baseDir}/references/frontend_best_practices.md`
3. **Run the appropriate script** when a project or component name is provided:
   ```bash
   # Scaffold a new Next.js or React project
   python {baseDir}/scripts/frontend_scaffolder.py my-app --template nextjs
   python {baseDir}/scripts/frontend_scaffolder.py my-app --template nextjs --features auth,api,forms,testing

   # Generate a component (client | server | hook) with optional test and story
   python {baseDir}/scripts/component_generator.py Button --dir src/components/ui
   python {baseDir}/scripts/component_generator.py UserProfile --type server --with-test --with-story

   # Analyze bundle for heavy dependencies and optimization opportunities
   python {baseDir}/scripts/bundle_analyzer.py ./project --verbose
   ```
4. **Emit the artifact**: component file, project structure, bundle report, or optimization recommendation.

## Output Contract

- Open with the classification and the primary issue or decision.
- Emit one primary artifact per response (component, config, or report).
- For bundle analysis: grade (A–F), list heavy packages with lighter alternatives.
- Annotate non-obvious TypeScript patterns or accessibility choices.
- Close with the next recommended step (e.g., "add Storybook story", "add `sizes` prop to Image").

## Key Rules

- Default to **Server Components** in Next.js. Add `'use client'` only when state, effects, or browser APIs are required.
- Default to **TypeScript** for all generated code.
- Use `cn()` from `@/lib/utils` for conditional Tailwind classes — not string concatenation.
- Every generated component must have explicit prop types; no implicit `any`.
- Bundle score below 70 (grade C or worse) triggers a dependency replacement recommendation.

## Proactive Triggers

Flag these without being asked:

- `moment` → replace with `date-fns` or `dayjs`
- `lodash` full import → switch to `lodash-es` with tree-shaking
- `COPY . .` before `npm install` in Dockerfile → reorder (defer to `docker-development`)
- Missing `alt` on `<img>` or `<Image>` → accessibility issue
- `useEffect` with data fetching in Next.js → suggest Server Component or `use()` hook
- No `sizes` on responsive `<Image>` → layout shift risk

## Guardrails

- Do not generate backend API routes or database schemas — stay within frontend scope.
- Do not add `'use client'` to components that only render static markup.
- Do not recommend `@mui/material` — prefer `shadcn/ui` or Radix UI primitives.
- For large-scale bundle or architecture concerns refer to `senior-architect`.
