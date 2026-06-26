import { Request, Response } from 'express';
import { NormalizedInboundMessage } from '../types';
import { ConnectorAdapter } from '../connectors/base';
import { ShadowService } from '../control-plane/shadow-service';

const isValidInbound = (body: Partial<NormalizedInboundMessage>) =>
  Boolean(body.source_type && body.source_thread_key && body.content);

export const processInboundMessage = async (
  message: NormalizedInboundMessage,
  deps: {
    shadowService: ShadowService;
  }
) => {
  return deps.shadowService.handleInbound(message);
};

export const inboundHandler =
  (shadowService: ShadowService) =>
  async (req: Request, res: Response) => {
    const body = req.body as Partial<NormalizedInboundMessage>;
    if (!isValidInbound(body)) {
      res.status(400).json({ error: 'source_type, source_thread_key, and content are required.' });
      return;
    }

    const result = await processInboundMessage(body as NormalizedInboundMessage, { shadowService });
    res.status(202).json(result);
  };

export const connectorInboundHandler =
  (connector: ConnectorAdapter, shadowService: ShadowService) =>
  async (req: Request, res: Response) => {
    const normalized = connector.normalize((req.body || {}) as Record<string, unknown>);
    const result = await processInboundMessage(normalized, { shadowService });
    res.status(202).json({
      connector: connector.source_type,
      normalized,
      ...result,
    });
  };
