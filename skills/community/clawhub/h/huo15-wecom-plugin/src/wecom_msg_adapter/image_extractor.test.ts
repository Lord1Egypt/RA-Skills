import { describe, it, expect } from "vitest";
import { extractMarkdownImages } from "./image_extractor.js";

describe("extractMarkdownImages", () => {
    it("extracts single image and leaves residual", () => {
        const r = extractMarkdownImages("Hello\n\n![cat](https://example.com/cat.png)\n\nSee above.");
        expect(r.images).toEqual([{ alt: "cat", url: "https://example.com/cat.png" }]);
        expect(r.residualText).toBe("Hello\n\nSee above.");
    });

    it("handles empty alt with 图片 placeholder", () => {
        const r = extractMarkdownImages("![](https://x/a.jpg)");
        expect(r.images).toEqual([{ alt: "图片", url: "https://x/a.jpg" }]);
        expect(r.residualText).toBe("");
    });

    it("extracts multiple images in order", () => {
        const r = extractMarkdownImages("a ![one](u1) b ![two](u2) c");
        expect(r.images).toEqual([
            { alt: "one", url: "u1" },
            { alt: "two", url: "u2" },
        ]);
        expect(r.residualText).toBe("a  b  c");
    });

    it("ignores title after url", () => {
        const r = extractMarkdownImages(`![a](https://x/a.png "title")`);
        expect(r.images[0]).toEqual({ alt: "a", url: "https://x/a.png" });
        expect(r.residualText).toBe("");
    });

    it("keeps normal links untouched", () => {
        const r = extractMarkdownImages("[link](https://x/)");
        expect(r.images).toEqual([]);
        expect(r.residualText).toBe("[link](https://x/)");
    });

    it("preserves reference-style images as-is", () => {
        const r = extractMarkdownImages("![a][ref]\n\n[ref]: https://x/r.png");
        expect(r.images).toEqual([]);
        expect(r.residualText).toContain("![a][ref]");
    });

    it("collapses consecutive blank lines left after image removal", () => {
        const r = extractMarkdownImages("line1\n\n![x](u)\n\nline2");
        expect(r.residualText).toBe("line1\n\nline2");
    });

    it("handles empty input", () => {
        expect(extractMarkdownImages("")).toEqual({ images: [], residualText: "" });
        expect(extractMarkdownImages(null as unknown as string)).toEqual({ images: [], residualText: "" });
    });

    it("preserves malformed image syntax", () => {
        const input = "![broken]()";
        const r = extractMarkdownImages(input);
        expect(r.images).toEqual([]);
    });
});
