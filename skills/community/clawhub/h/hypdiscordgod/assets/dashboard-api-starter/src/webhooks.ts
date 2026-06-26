import { Router } from 'express';
import { enqueueJob } from './jobs.js';

export const webhookRouter = Router();

webhookRouter.post('/webhooks/example', (req, res) => {
  const expected = process.env.WEBHOOK_SHARED_SECRET;
  const provided = req.header('x-webhook-secret');
  if (!expected || provided !== expected) {
    res.status(401).json({ error: 'unauthorized' });
    return;
  }

  const jobId = enqueueJob('example.webhook', req.body);
  res.json({ ok: true, jobId });
});
