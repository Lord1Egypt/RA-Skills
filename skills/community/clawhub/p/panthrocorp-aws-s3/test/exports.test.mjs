import { describe, it } from "node:test";
import { strict as assert } from "node:assert";
import { createRequire } from "node:module";

const require = createRequire(import.meta.url);
const mod = require("../dist/index.cjs");

describe("aws-s3 bundle exports", () => {
  it("exports S3Client as a constructor", () => {
    assert.equal(typeof mod.S3Client, "function");
  });

  it("exports ListObjectsV2Command", () => {
    assert.equal(typeof mod.ListObjectsV2Command, "function");
  });

  it("exports GetObjectCommand", () => {
    assert.equal(typeof mod.GetObjectCommand, "function");
  });

  it("exports PutObjectCommand", () => {
    assert.equal(typeof mod.PutObjectCommand, "function");
  });

  it("exports DeleteObjectCommand", () => {
    assert.equal(typeof mod.DeleteObjectCommand, "function");
  });

  it("exports HeadObjectCommand", () => {
    assert.equal(typeof mod.HeadObjectCommand, "function");
  });

  it("can instantiate S3Client without network calls", () => {
    const client = new mod.S3Client({ region: "us-east-1" });
    assert.ok(client);
    client.destroy();
  });
});
