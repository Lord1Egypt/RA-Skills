import Fastify from "fastify";
import { BhmailerHttpAdapter } from "./adapters/mail/bhmailer_http";
import { MockMailAdapter } from "./adapters/mail/mock";
import type { MailQueryAdapter } from "./adapters/mail/types";
import { loadConfig } from "./config/schema";
import { registerRoutes } from "./routes/register";
import { JobCoordinator } from "./services/coordinator";
import { SQLiteStore } from "./state/sqlite";

function buildMailAdapter(config: ReturnType<typeof loadConfig>): MailQueryAdapter {
  if (config.mail.backend === "bhmailer-http") {
    return new BhmailerHttpAdapter({
      baseUrl: config.mail.bhmailerApiBase,
      uid: config.mail.uid,
      sign: config.mail.sign,
      defaultTimeoutSec: config.mail.defaultTimeoutSec,
      extractionProfile: config.mail.extractionProfile,
      maxRetries: 2
    });
  }

  return new MockMailAdapter();
}

async function main(): Promise<void> {
  const config = loadConfig();
  const app = Fastify({
    logger: {
      level: "info"
    }
  });

  const store = new SQLiteStore(config.bridge.sqlitePath);
  const mailAdapter = buildMailAdapter(config);
  const coordinator = new JobCoordinator(store, config, mailAdapter);
  const sweepTimer = setInterval(() => {
    coordinator
      .runMaintenance()
      .then((result) => {
        if (
          result.sweptWatches > 0 ||
          result.requeuedClaims > 0 ||
          result.inboundDedupePruned > 0 ||
          result.webhookDedupePruned > 0
        ) {
          app.log.info({ result }, "bridge maintenance run");
        }
      })
      .catch((error) => {
        const message = error instanceof Error ? error.message : String(error);
        app.log.error({ err: message }, "failed to run maintenance");
      });
  }, config.bridge.sweepIntervalSec * 1000);

  await registerRoutes(app, {
    config,
    store,
    coordinator,
    mailAdapter
  });

  app.addHook("onClose", async () => {
    clearInterval(sweepTimer);
    store.close();
  });

  await app.listen({
    host: config.server.host,
    port: config.server.port
  });
}

main().catch((error) => {
  const message = error instanceof Error ? error.stack ?? error.message : String(error);
  process.stderr.write(`${message}\n`);
  process.exit(1);
});
