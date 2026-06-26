import crypto from 'node:crypto';
import type { Request, Response, NextFunction } from 'express';

export function issueCsrfToken(req: Request, res: Response, next: NextFunction) {
  if (!req.signedCookies.csrf_token) {
    res.cookie('csrf_token', crypto.randomUUID(), {
      httpOnly: false,
      sameSite: 'lax',
      secure: false,
      signed: true
    });
  }
  next();
}

export function requireCsrf(req: Request, res: Response, next: NextFunction) {
  const cookieToken = req.signedCookies.csrf_token;
  const headerToken = req.header('x-csrf-token');
  if (!cookieToken || !headerToken || cookieToken !== headerToken) {
    res.status(403).json({ error: 'csrf_failed' });
    return;
  }
  next();
}
