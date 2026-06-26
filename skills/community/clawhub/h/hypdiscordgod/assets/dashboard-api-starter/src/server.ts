import 'dotenv/config';
import cookieParser from 'cookie-parser';
import cors from 'cors';
import express from 'express';
import { issueCsrfToken } from './csrf.js';
import { router } from './routes.js';
import { webhookRouter } from './webhooks.js';

const app = express();
app.use(cors({ origin: true, credentials: true }));
app.use(cookieParser(process.env.SESSION_COOKIE_SECRET || 'dev-secret'));
app.use(express.json());
app.use(issueCsrfToken);
app.use(router);
app.use(webhookRouter);

const port = Number(process.env.PORT || 3000);
app.listen(port, () => {
  console.log(`Dashboard/API starter listening on ${port}`);
});
