# Kanban + Detail Recipes

## Recipe 1: Hook-first board

```tsx
import { CKanbanBoard, useKanbanBoard } from 'orbcafe-ui';

const kanban = useKanbanBoard({
  initialBuckets: buckets,
  initialCards: cards,
  onCardMove: ({ cardId, toBucketId }) => {
    syncStatus(cardId, toBucketId);
  },
});

<CKanbanBoard {...kanban.boardProps} />;
```

## Recipe 2: Click card into DetailInfo

```tsx
<CKanbanBoard
  {...kanban.boardProps}
  onCardClick={({ card, bucket }) => {
    const params = new URLSearchParams({
      source: 'kanban',
      bucket: bucket.id,
      bucketTitle: bucket.title,
      backHref: '/kanban',
    });
    router.push(`/detail-info/${card.id}?${params.toString()}`);
  }}
/>
```

## Recipe 3: Reducer/store tool path

```tsx
import { createKanbanBoardModel, moveKanbanCard } from 'orbcafe-ui';

const initialModel = createKanbanBoardModel({ buckets, cards });
const nextModel = moveKanbanCard(initialModel, {
  cardId: 'TASK-203',
  fromBucketId: 'intake',
  toBucketId: 'execution',
  targetIndex: 0,
});
```
