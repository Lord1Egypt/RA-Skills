# Look Command Reference

## look.ingest.image
Inputs: image(s), optional EXIF, optional device_preparse, ingest_source.
Outputs: ingest record, DecisionRecord(ingest).

## look.propose.actions
Inputs: optional ingest_id, optional user hint.
Outputs: Report containing 1-3 ActionDrafts plus DecisionRecords for each stage (ingest, context, route, research, reduce, draft).

## look.execute.action
Inputs: draft_id, explicit confirmation token.
Outputs: ExecutionReceipt, DecisionRecord(execute). Rejects high-risk without confirmation.

## look.rollback.action
Inputs: execution_id.
Outputs: updated ExecutionReceipt, DecisionRecord(rollback). Attempts reversal for reversible actions.

## look.status
Outputs: last ingest summary, pending drafts, items awaiting clarification or confirmation.

## look.config.set
Inputs: config patch. Outputs: DecisionRecord(config).
