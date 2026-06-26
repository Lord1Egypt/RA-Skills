import { createApp } from "./app";

const port = Number(process.env.PORT ?? 4800);
const app = createApp();

app.listen(port, () => {
  console.log(`OpenClaw gateway running on http://localhost:${port}`);
});
