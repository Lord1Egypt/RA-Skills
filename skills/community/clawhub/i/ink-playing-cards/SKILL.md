---
name: ink-playing-cards
description: "Use when building terminal card games with ink-playing-cards, working with card components, deck management, zone systems, event systems, effect systems, or any card game logic using Ink and React for CLI rendering."
---

# ink-playing-cards v1.0.0

React component library for terminal-based card games with Ink 6 (React 19 for CLIs). Provides UI components, hooks, contexts, and game systems.

```bash
npm install ink-playing-cards
# deps: ink ^6.0.0, react ^19.0.0 — requires Node >= 20
```

## Architecture

All state flows through `DeckProvider` (React context + `useReducer`). Zones are immutable `TCard[]` arrays. The `useDeck` hook wraps dispatch.

```text
DeckProvider
├── zones.deck: TCard[]
├── zones.hands: Record<string, TCard[]>
├── zones.discardPile: TCard[]
├── zones.playArea: TCard[]
├── zones.custom: Record<string, TCard[]>   // arbitrary named zones (tableau, foundation, ...)
├── players: string[]
├── eventManager / effectManager
└── dispatch(DeckAction)
```

Custom zones are addressed by name via `moveCard`/`setZone`/`clearZone`/`getZone` — useful for games (solitaire, etc.) that need more structure than deck/hand/discard/play. See `MOVE_CARD`/`SET_ZONE`/`CLEAR_ZONE` below.

## Quick Start

```tsx
import React from 'react'
import { render, Box, Text, useInput } from 'ink'
import { DeckProvider, useDeck, useHand, CardStack } from 'ink-playing-cards'

const Game = () => {
  const { deck, shuffle, draw } = useDeck()
  const { hand, playCard, discard } = useHand('player1')

  React.useEffect(() => { shuffle(); draw(5, 'player1') }, [])
  useInput((input) => { if (input === 'd') draw(1, 'player1') })

  return (
    <Box flexDirection="column">
      <Text>Deck: {deck.length}</Text>
      <CardStack cards={hand} name="Hand" isFaceUp maxDisplay={5} />
    </Box>
  )
}

render(<DeckProvider><Game /></DeckProvider>)
```

## Types

```ts
type TCard = (CardProps | CustomCardProps) & { id: string }  // every card has a unique `id`

type BaseCardProps = {
  // `id` is optional here — only required on `TCard` (zone bookkeeping,
  // React keys). A single decorative `<Card>`/`<CustomCard>` doesn't need one.
  id?: string; effects?: CardEffect[]; faceUp?: boolean; selected?: boolean; rounded?: boolean
}

type CardProps = BaseCardProps & {
  suit: 'hearts' | 'diamonds' | 'clubs' | 'spades'
  value: '2' | '3' | ... | 'K' | 'A' | 'JOKER'
  theme?: AsciiTheme  // 'original' | 'geometric' | 'animal' | 'robot' | 'pixel' | 'medieval'
}

type CustomCardProps = BaseCardProps & {
  size?: 'micro' | 'mini' | 'small' | 'medium' | 'large'  // or explicit width/height
  title?: string; cost?: string              // header row
  asciiArt?: string; artColor?: string       // art region
  typeLine?: string                          // between art and body
  description?: string                       // body (auto-wraps)
  footerLeft?: string; footerRight?: string  // footer row
  symbols?: CustomCardSymbol[]               // corner symbols
  content?: ReactNode                        // freeform mode — overrides all regions
  back?: CustomCardBack                      // { art?, symbol?, color?, label? }
  borderColor?: string; textColor?: string
  value?: TCardValue | string; type?: string // game logic metadata (not rendered)
}

// Type guards
function isStandardCard(card: TCard): card is CardProps
function isCustomCard(card: TCard): card is CustomCardProps
function generateCardId(suit: TSuit, value: TCardValue): string  // "hearts-A-<rand6>"
```

## Hooks

### useDeck — must be inside `<DeckProvider>`

```ts
const {
  // State
  deck,          // TCard[]
  hands,         // Record<string, TCard[]>
  discardPile,   // TCard[]
  playArea,      // TCard[]
  customZones,   // Record<string, TCard[]> — named zones, keyed by name
  players,       // string[]
  backArtwork,   // { ascii, simple, minimal }
  eventManager,  // EventManager
  effectManager, // EffectManager
  // Actions
  shuffle,          // () => void
  draw,             // (count, playerId) => void — auto-registers player
  deal,             // (count, playerIds[]) => void — auto-registers players
  reset,            // (cards?) => void
  cutDeck,          // (index) => void
  addPlayer,        // (id) => void
  removePlayer,     // (id) => void
  getPlayerHand,    // (id) => TCard[]
  addCustomCard,    // (card: CustomCardProps) => void
  removeCustomCard, // (cardId) => void
  setBackArtwork,   // (Partial<BackArtwork>) => void
  moveCard,         // (cardId, from, to, position?) => void — move between any two zones
  setZone,          // (name, cards) => void — seed/overwrite a custom zone
  clearZone,        // (name) => void — remove a custom zone
  getZone,          // (name) => TCard[] — read any zone (built-in or custom) by name
} = useDeck()
```

`draw()` and `deal()` dispatch actions — they do NOT return cards. Access drawn cards via `hands[playerId]` after re-render.

### useHand(playerId) — convenience wrapper

```ts
const { hand, drawCard, playCard, discard } = useHand('player1')
// hand: TCard[]
// drawCard(count = 1) — draws from deck
// playCard(cardId: string) — hand → playArea
// discard(cardId: string) — hand → discardPile
```

### useGame — must be inside `<GameProvider>`

```ts
const {
  currentPlayerId, players, turn, phase, dispatch,
  setCurrentPlayer,   // (playerId: string) => void
  nextTurn,           // () => void — next player, turn++
  setPhase,           // (phase: string) => void
} = useGame()
```

## Components

### Card — standard playing card

Variants: `simple` (11×9, default), `ascii` (15×13, themed face cards), `minimal` (6×5).

```tsx
<Card id="h-A-1" suit="hearts" value="A" variant="simple" faceUp selected rounded theme="original" />
```

### MiniCard — compact card

Variants: `mini` (5×4, default), `micro` (4×4). Same props as `CardProps` plus `variant`.

```tsx
<MiniCard id="s-K-1" suit="spades" value="K" variant="mini" faceUp />
```

### UnicodeCard — single character

Unicode playing card characters. Auto-colors red/white by suit.

```tsx
<UnicodeCard suit="hearts" value="A" faceUp bordered rounded size={1} dimmed color="red" />
```

### CustomCard — non-standard cards

Two modes: structured (title/cost/art/typeLine/description/footer regions) or freeform (`content` ReactNode).
Size presets: `micro` (5×3), `mini` (8×5), `small` (12×7), `medium` (18×11, default), `large` (24×15). Override with `width`/`height`.

```tsx
<CustomCard id="c1" size="large" title="Dragon" cost="{4}{R}"
  asciiArt={art} typeLine="Creature" description="Flying"
  footerLeft="5/5" borderColor="red" />

<CustomCard id="c2" content={<Text>Freeform</Text>} />
<CustomCard id="c3" faceUp={false} back={{ art: '♠♠♠', color: 'cyan' }} />
```

### TarotCard — tarot deck cards

Wraps `CustomCard` with tarot-specific semantics. Uses a discriminated union on `arcana` for Major vs Minor Arcana. Renders a 20×13 card with themed defaults.

Standard 78-card tarot deck: 22 Major Arcana + 56 Minor Arcana (14 per suit × 4 suits).
Tarot suits: `wands` (🜂), `cups` (☽), `swords` (⚔), `pentacles` (⛤).
Minor values: `Ace`–`10` + `Page`, `Knight`, `Queen`, `King`.

```tsx
import { TarotCard, createTarotDeck } from 'ink-playing-cards'

// Major Arcana (index 0–21: The Fool through The World)
<TarotCard id="fool" arcana="major" majorIndex={0} />
<TarotCard id="tower" arcana="major" majorIndex={16} reversed />

// Minor Arcana
<TarotCard id="ace-cups" arcana="minor" suit="cups" value="Ace" />
<TarotCard id="qw" arcana="minor" suit="wands" value="Queen" reversed />

// Face down with custom tarot back
<TarotCard id="hidden" arcana="major" majorIndex={13} faceUp={false} />

// Custom styling
<TarotCard id="devil" arcana="major" majorIndex={15}
  borderColor="red" textColor="red" artColor="red" />
```

Props (Major): `arcana="major"`, `majorIndex` (0–21), `reversed?`, `asciiArt?`, `borderColor?`, `textColor?`, `artColor?`, `back?`, plus all `BaseCardProps`.

Props (Minor): `arcana="minor"`, `suit` (`TarotSuit`), `value` (`TarotMinorValue`), `reversed?`, `asciiArt?`, `borderColor?`, `textColor?`, `artColor?`, `back?`, plus all `BaseCardProps`.

Types: `TarotCardProps`, `TarotMajorProps`, `TarotMinorProps`, `TarotSuit`, `TarotMinorValue`, `MajorArcanaIndex`.

Defaults: Major Arcana uses yellow border / magenta art. Minor Arcana uses cyan border / cyan art. All 22 Major Arcana have built-in ASCII art. Minor pip cards auto-generate suit symbol art. `reversed` shows "⟳ Reversed" on the type line.

### CardStack — overlapping card list

Renders `TCard[]` with overlap. Handles both standard and custom cards.

```tsx
<CardStack cards={hand} name="Hand" isFaceUp maxDisplay={5}
  variant="simple" stackDirection="horizontal"
  spacing={{ overlap: -2, margin: 1 }} alignment="start" />
```

Defaults: `isFaceUp: false`, `maxDisplay: 3`, `stackDirection: 'vertical'`, `variant: 'simple'`.

### CardGrid — grid layout (standard cards only)

```tsx
import { CardGrid, type GridCard } from 'ink-playing-cards'
// GridCard = { id: string, suit: TSuit, value: TCardValue }

<CardGrid rows={4} cols={4} cards={gridCards} variant="simple"
  isFaceUp fillEmpty spacing={{ row: 1, col: 1, margin: 1 }} />
```

`alignment.vertical` (`'top' | 'middle' | 'bottom'`) is a no-op unless an explicit `height` prop is also passed — without it, the column container has no extra main-axis space to distribute:

```tsx
<CardGrid rows={2} cols={3} cards={gridCards} height={20}
  alignment={{ horizontal: 'center', vertical: 'bottom' }} />
```

### Deck — visual deck display

Must be inside `DeckProvider`. Shows top card + placeholder.

```tsx
<Deck variant="simple" showTopCard placeholderCard={{ suit: 'hearts', value: 'A' }} />
```

## Contexts

### DeckProvider

```tsx
<DeckProvider initialCards={myCards} customReducer={myReducer}>
  <Game />
</DeckProvider>
```

Default deck: 52 cards via `createStandardDeck()`. Pass `customReducer` to extend — note the built-in `deckReducer` is NOT exported; replicate needed cases or use `Zones` utilities.

### GameProvider — turn management (separate from DeckProvider)

```tsx
<GameProvider initialPlayers={['alice', 'bob']} customReducer={myGameReducer}>
  <DeckProvider><Game /></DeckProvider>
</GameProvider>

// Access: useGame()
const { currentPlayerId, players, turn, phase, nextTurn, setPhase, setCurrentPlayer } = useGame()
nextTurn()                       // next player, turn++
setPhase('playing')
setCurrentPlayer('bob')
```

## Event System

Events dispatch automatically from the reducer. Subscribe via `eventManager` from `useDeck()`.

```ts
const { eventManager } = useDeck()
const listener = {
  handleEvent(event: GameEventData) { /* event.type, .playerId, .card, .cards, .count */ }
}
eventManager.addEventListener('CARDS_DRAWN', listener)
eventManager.removeEventListener('CARDS_DRAWN', listener)
eventManager.dispatchEvent({ type: 'CUSTOM_EVENT', playerId: 'p1' })  // custom events OK
eventManager.removeAllListeners()
```

Built-in events: `DECK_SHUFFLED`, `CARDS_DRAWN` (playerId, cards), `CARDS_DEALT` (playerId, cards, count — per player), `CARD_PLAYED` (playerId, card), `CARD_DISCARDED` (playerId, card), `CARD_MOVED` (card, from, to), `DECK_RESET`, `DECK_CUT`.

## Effect System

Attach abilities to cards. All implement `CardEffect.apply(gameState, eventData)`.

```ts
import { Effects } from 'ink-playing-cards'

new Effects.DrawCardEffect(2)                              // deck → hand
new Effects.DamageEffect(3)                                // target.life or .health
new Effects.ConditionalEffect(condFn, effect)              // fires when condition true
new Effects.TriggeredEffect('CARD_PLAYED', effect)         // fires on event match
new Effects.DelayedEffect(3, effect)                       // fires after N turns
new Effects.TargetedEffect(selectorFn, effect)             // selects target from gameState
new Effects.ContinuousEffect(condFn, applyFn, removeFn)   // toggle on condition

Effects.attachEffectToCard(card, effect)                   // pushes to card.effects[]
effectManager.applyCardEffects(card, gameState, eventData) // runs all effects on card
```

Effects mutate `gameState`/`eventData` directly — designed for effect pipelines, not reducer use.

## Zone Utilities

```ts
import { Zones, createStandardDeck, createPairedDeck, createTarotDeck } from 'ink-playing-cards'

// Pure functions (immutable, safe for reducers)
Zones.shuffleCards(cards)        // Fisher-Yates, new array
Zones.drawCards(cards, count)    // [drawn, remaining] — draws from end
Zones.addCard(cards, card)       // append
Zones.addCards(cards, newCards)   // append multiple
Zones.removeCard(cards, cardId)  // filter by id
Zones.findCard(cards, cardId)    // find by id
Zones.cutDeck(cards, index)      // split and reorder

// Deck creation
createStandardDeck()             // 52 cards with unique IDs
createPairedDeck(shuffle?)       // paired deck for Memory games
createTarotDeck()                // 78-card tarot deck (22 Major + 56 Minor Arcana)

// Legacy class API (mutable): Zones.Deck, Zones.Hand, Zones.DiscardPile, Zones.PlayArea
// Each has addCard(), removeCard(), shuffle(). Deck also has drawCard(), drawCards(n).
```

## DeckAction / GameAction (for custom reducers)

```ts
type DeckAction =
  | { type: 'SHUFFLE' }
  | { type: 'DRAW'; payload: { count: number; playerId: string } }
  | { type: 'DEAL'; payload: { count: number; playerIds: string[] } }
  | { type: 'RESET'; payload?: { cards?: TCard[] } }
  | { type: 'CUT_DECK'; payload: number }
  | { type: 'PLAY_CARD'; payload: { playerId: string; cardId: string } }
  | { type: 'DISCARD'; payload: { playerId: string; cardId: string } }
  | { type: 'ADD_PLAYER'; payload: string }
  | { type: 'REMOVE_PLAYER'; payload: string }
  | { type: 'ADD_CUSTOM_CARD'; payload: CustomCardProps }
  | { type: 'REMOVE_CUSTOM_CARD'; payload: { cardId: string } }
  | { type: 'SET_BACK_ARTWORK'; payload: Partial<BackArtwork> }
  | { type: 'MOVE_CARD'; payload: { cardId: string; from: ZoneName; to: ZoneName; position?: 'top' | 'bottom' | number } }
  | { type: 'SET_ZONE'; payload: { name: string; cards: TCard[] } }
  | { type: 'CLEAR_ZONE'; payload: { name: string } }

type GameAction =
  | { type: 'SET_CURRENT_PLAYER'; payload: string }
  | { type: 'NEXT_TURN' }
  | { type: 'SET_PHASE'; payload: string }
```

## Gotchas

- `draw()`/`deal()` are async via dispatch — cards appear in `hands[playerId]` on next render, not as return values.
- Every card needs a unique `id`. Use `generateCardId()` or your own scheme.
- `useHand.playCard(cardId)` and `discard(cardId)` take a string ID, not a card object.
- `isStandardCard(card)` type guard is required before accessing `.suit`/`.value` on a `TCard`.
- The built-in `deckReducer` is not exported. Custom reducers receive `(DeckContextType, DeckAction)` and must handle all cases or delegate to `Zones` utilities.
- `DeckProvider` and `GameProvider` are separate contexts — use both for full game state.
