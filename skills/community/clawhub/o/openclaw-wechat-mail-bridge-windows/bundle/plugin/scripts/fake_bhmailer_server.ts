import Fastify from "fastify";

async function main(): Promise<void> {
  const app = Fastify({ logger: true });

  app.post("/mailFind", async (request) => {
    const body = request.body as Record<string, unknown> | undefined;
    const email = String(body?.email ?? "");
    return {
      ok: true,
      data: {
        found: true,
        matchedEmail: email,
        mailId: "fake_mail_001",
        subject: "Fake BHMailer mail",
        from: "fake@example.com",
        receivedAt: new Date().toISOString(),
        bodyPreview: "This is fake BHMailer payload."
      }
    };
  });

  app.post("/mailReceive", async (request) => {
    const body = request.body as Record<string, unknown> | undefined;
    const email = String(body?.email ?? "");
    return {
      ok: true,
      data: {
        found: true,
        matchedEmail: email,
        mailId: "fake_mail_002",
        subject: "Fake BHMailer receive",
        from: "fake@example.com",
        receivedAt: new Date().toISOString(),
        bodyPreview: "This is fake BHMailer receive payload."
      }
    };
  });

  app.post("/mailExtract", async () => {
    return {
      ok: true,
      data: {
        extractedFields: {
          code: "112233"
        }
      }
    };
  });

  await app.listen({ host: "127.0.0.1", port: 39015 });
}

main().catch((error) => {
  process.stderr.write(`${error instanceof Error ? error.stack ?? error.message : String(error)}\n`);
  process.exit(1);
});

