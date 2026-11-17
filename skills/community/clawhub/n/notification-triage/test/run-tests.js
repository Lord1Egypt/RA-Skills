module.exports = [
  { name: "no args shows status", args: [], expected: "[notify-triage] Status" },
  { name: "--rules shows configured rules", args: ["--rules"], expected: "Current rules" },
  { name: "--status shows status", args: ["--status"], expected: "[notify-triage] Status" },
  { name: "invalid arg shows status", args: ["--bogus"], expected: "[notify-triage] Status" },
  { name: "--classify shows usage when missing args", args: ["--classify"], expected: "Usage:" }
];
