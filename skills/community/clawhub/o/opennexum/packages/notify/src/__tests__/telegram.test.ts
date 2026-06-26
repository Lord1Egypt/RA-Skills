import assert from "node:assert/strict";
import { mock } from "node:test";
import test from "node:test";

// Mock execa before importing sendMessage
let execaArgs: string[][] = [];
let execaThrows = false;

mock.module("execa", {
  namedExports: {
    execa: async (...args: string[]) => {
      execaArgs.push(args);
      if (execaThrows) throw new Error("openclaw failed");
    },
  },
});

const { sendMessage } = await import("../telegram.js");

test("sendMessage calls openclaw with correct arguments", async () => {
  execaArgs = [];
  execaThrows = false;

  await sendMessage("my-target", "hello world");

  assert.equal(execaArgs.length, 1);
  assert.deepEqual(execaArgs[0], [
    "openclaw",
    ["message", "send", "--target", "my-target", "--message", "hello world"],
  ]);
});

test("sendMessage does not throw when openclaw fails", async () => {
  execaArgs = [];
  execaThrows = true;

  await assert.doesNotReject(async () => {
    await sendMessage("my-target", "hello world");
  });

  execaThrows = false;
});
