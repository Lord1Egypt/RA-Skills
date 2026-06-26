# AI Module Contracts

This file is the AI-facing source of truth for module selection, public API shape, hook strategy, canonical examples, and verification expectations.

Machine-readable sibling:
- `module-contracts.json`

Use it before reading a module README in detail.

## 1. StdReport

- Public entry:
  - `CStandardPage`
  - `CTable`
  - `CSmartFilter`
  - `CLayoutManager`
  - `CVariantManager`
  - `useStandardReport`
- Preferred pattern:
  - `useStandardReport + CStandardPage mode="integrated"`
- Hooks:
  - Public hook exists: `useStandardReport`
- Minimal state contract:
  - report identity: `metadata.id` / `id` / `appId`
  - filters state
  - pagination state
  - rows + total
- Canonical example:
  - `examples/app/_components/StdReportExampleClient.tsx`
  - `examples/app/std-report/page.tsx`
- Verify:
  - filter applies
  - page changes
  - variant/layout persists
  - quick actions fire
- Common failure modes:
  - missing identity
  - no `npm run build` in local `file:..` flow
  - wrong import path

## 2. GraphReport / DetailInfo / CustomizeAgent

- Public entry:
  - `CGraphReport`
  - `useGraphReport`
  - `CDetailInfoPage`
  - `useDetailInfo`
  - `CCustomizeAgent`
- Preferred pattern:
  - detail: `Server page await params -> Client page`
  - graph: table-integrated graph entry first
  - settings: one-shot `onSaveAll`
- Hooks:
  - Public hooks exist:
    - `useGraphReport`
    - `useGraphChartData`
    - `useGoogleMapEmbedUrl`
    - `useAmapEmbedUrl`
    - `useGraphInteraction`
    - `useDetailInfo`
- Minimal state contract:
  - graph open/model/tableContent
  - detail sections/tabs/search query/AI fallback
  - settings value + template ids
- Canonical example:
  - `examples/app/detail-info/[id]/DetailInfoExampleClient.tsx`
- Verify:
  - graph interaction works
  - detail search hits fields
  - AI fallback returns
  - settings save fully applies
- Common failure modes:
  - controlled graph props missing
  - detail AI fallback not wired
  - settings partially persisted

## 3. Layout / Navigation

- Public entry:
  - `CAppPageLayout`
  - `CAppHeader`
  - `usePageLayout`
  - `NavigationIsland`
  - `TreeMenu`
  - `useNavigationIsland`
  - `CPageTransition`
- Preferred pattern:
  - `examples/app/layout.tsx` + `providers.tsx` shell first
- Hooks:
  - Public hooks exist:
    - `usePageLayout`
    - `useNavigationIsland`
- Minimal state contract:
  - menu data
  - user/menu actions
  - locale/theme mounted safety
- Canonical example:
  - `examples/app/layout.tsx`
  - `examples/app/providers.tsx`
- Verify:
  - nav works
  - locale switches
  - user menu works
  - no hydration mismatch
- Common failure modes:
  - `usePathname` used unsafely on first render
  - provider stack missing
  - client/server route boundary incorrect

## 4. PivotTable / AINav

- Public entry:
  - `CPivotTable`
  - `usePivotTable`
  - `CAINavProvider`
  - `useAINav`
  - `useVoiceInput`
- Preferred pattern:
  - pivot persistence: controlled hook mode
  - AINav: provider wrapper with required submit callback
- Hooks:
  - Public hooks exist:
    - `usePivotTable`
    - `useVoiceInput`
    - `useAINav`
- Minimal state contract:
  - pivot rows/columns/measures/presets
  - AINav recording/submission state
- Canonical example:
  - `examples/app/_components/PivotTableExampleClient.tsx`
  - `examples/app/_components/AINavExampleClient.tsx`
- Verify:
  - drag/drop layout changes
  - aggregation changes
  - presets persist
  - voice submit callback fires
- Common failure modes:
  - uncontrolled pivot state where persistence is needed
  - no `onVoiceSubmit`
  - localStorage read/write in wrong render phase

## 5. AgentUI

- Public entry:
  - `AgentPanel`
  - `StdChat`
  - `CopilotChat`
  - `type ChatMessage`
  - `type AgentUICardHooks`
- Preferred pattern:
  - full page chat: `AgentPanel` or `StdChat`
  - floating helper: `CopilotChat` inside custom shell
- Hooks:
  - No public custom hook
  - Use props + callback contracts instead
- Minimal state contract:
  - `messages`
  - `isResponding`
  - assistant `isStreaming`
  - for copilot shell: `isOpen`, `corner`, `panelSize`, `panelPosition`
- Canonical example:
  - `examples/app/chat/ChatExampleClient.tsx`
  - `examples/app/copilot/CopilotExampleClient.tsx`
- Verify:
  - send appends user message
  - assistant streams
  - `onMessageStreamingComplete` clears streaming flag
  - card actions emit `cardHooks.onCardEvent`
  - copilot open/close/drag/resize works when shell exists
- Common failure modes:
  - treating `CopilotChat` as full floating system
  - forgetting `isStreaming` lifecycle
  - coupling to internal renderers
  - resize observer overwriting shell resize state

## 6. Shared Rules For AI

- Import only from `orbcafe-ui`.
- Prefer the canonical example before inventing a new composition.
- If public hooks exist, use the hook README after the module contract.
- If no public hook exists, do not invent one; use the public component plus callbacks.
- Every final answer or implementation plan should include:
  - chosen module
  - paste-ready public import
  - minimal state contract
  - verify checklist
  - troubleshooting checklist
