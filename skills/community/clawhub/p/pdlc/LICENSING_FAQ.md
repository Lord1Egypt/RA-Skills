# Licensing FAQ — AIFLC (AI Full Life Cycle)

> **DRAFT — Pending review before publication**

---

## General Questions

### Q: Is AIFLC open source?

**A:** Yes. The **PDLC family** of AIFLC — the family published in this repository — is licensed under the **Apache License 2.0 with an Attribution Addendum**, an OSI-approved open source license. You are free to use, modify, and distribute the PDLC family for any purpose, including commercial use, at no cost. (AIFLC is licensed per family; this answer covers the PDLC family.)

---

### Q: Which packages are covered?

**A:** AI-ILC, AI-PILC, AI-PPM, AI-FLO, AI-ADLC, AI-UXD, AI-POLC, AI-DWG, AI-GCE, AI-TGE, and AI-DFE. Together these eleven packages form the **PDLC family** of AIFLC — the family published in this repository. AI-DLC v1 is **not** part of AIFLC — it is an AWS product (awslabs/aidlc-workflows) licensed separately under MIT-0.

This License governs the PDLC family only. AIFLC is licensed **per family**: other AIFLC families are published as separate repositories that may carry their own license terms.

---

### Q: Are all AIFLC families free and open?

**A:** Not necessarily. AIFLC is organised into families, and licensing is decided **per family**. The PDLC family published here is free and open under Apache 2.0 + Attribution. Other AIFLC families are separate repositories with their own terms — adopting this family grants no rights to any other family.

---

### Q: What license does AIFLC use?

**A:** Apache License 2.0, with an Attribution Addendum. The Apache 2.0 base is the same license used by Kubernetes, Android, and the Apache Software Foundation projects. The Attribution Addendum adds one additional condition: any product or service built on AIFLC must include a visible notice crediting the original work.

---

### Q: Who owns AIFLC?

**A:** AIFLC is created and owned by **Mohammad Maheri** (Copyright © 2026 Mohammad Maheri). The Apache 2.0 license grants you broad rights to use and build on it — ownership of the original work remains with the author.

---

## Using AIFLC

### Q: Can I download and use AIFLC for free?

**A:** Yes — for any purpose, including commercial use. There are no license fees, no tiers, and no usage restrictions beyond the Attribution Addendum.

---

### Q: Can I use AIFLC in my company for commercial projects?

**A:** Yes, freely. You can use AIFLC to run internal projects, deliver client engagements, or build commercial products — all without purchasing anything.

---

### Q: Can I modify AIFLC?

**A:** Yes. You can fork, modify, and adapt AIFLC for any purpose. Modified versions must carry notices stating what was changed (Apache 2.0 Section 4(b)) and must retain the original copyright and license notices.

---

### Q: Can I embed AIFLC in a commercial product or SaaS platform?

**A:** Yes. Apache 2.0 explicitly permits this. You must retain the license and copyright notices, and comply with the Attribution Addendum (see below).

---

### Q: Can I sell a product or service built on AIFLC?

**A:** Yes. Apache 2.0 permits commercial use and distribution without restriction, including selling modified versions. The Attribution Addendum applies — your product must credit the original work.

---

### Q: Can I use AIFLC as the core material in a paid training course?

**A:** Yes. No license fee is required. The Attribution Addendum applies — course materials must include the attribution notice.

---

## The Attribution Addendum

### Q: What is the Attribution Addendum?

**A:** It is an additional condition on top of Apache 2.0. Any product, service, platform, or deliverable that substantially incorporates or is based on AIFLC must include the following notice in a prominent location (README, documentation, about page, or equivalent):

> *Built on AIFLC by Mohammad Maheri — [LinkedIn](https://www.linkedin.com/in/mohammad-maheri-8399565b)*

---

### Q: Where exactly does the attribution notice need to appear?

**A:** In at least one location that is reasonably visible to end users or downstream recipients. This includes README files, product documentation, user-facing about pages, application footers, or equivalent. It does not need to appear in every file — one prominent location per distributed product is sufficient.

---

### Q: Does the attribution apply to internal use?

**A:** If you are using AIFLC internally and not distributing a product or service to others, the Attribution Addendum does not apply. It is triggered by distribution — sharing, publishing, selling, or deploying a product to users outside your organisation.

---

### Q: What happens if I don't include the attribution notice?

**A:** Failure to include the required notice is a material breach of the license. Your rights under the license terminate automatically. You have a 30-day cure window to add the notice and reinstate your rights — but only for a first breach. See `NOTICE` for full attribution terms.

---

### Q: Does the attribution notice imply that Mohammad Maheri endorses my product?

**A:** No. The notice is for attribution only. It does not imply endorsement, sponsorship, certification, or approval of your product by the author. See `NOTICE` for the no-endorsement clause.

---

## Contributing

### Q: Can I contribute improvements back to AIFLC?

**A:** Yes — contributions are welcome. You must sign the Contributor License Agreement (CLA) before your contribution can be accepted. See `CLA.md`.

---

### Q: Why is a CLA required if the license is already open?

**A:** The CLA ensures the author retains the right to maintain, relicense, and build commercial services on top of AIFLC — including contributions made by others. It does not take away your ownership of your contribution. You retain copyright; the CLA grants the author the right to include and distribute your contribution under the current and any future license the project adopts.

---

### Q: If I contribute code, who owns it?

**A:** You retain copyright ownership of your contribution. The CLA grants Mohammad Maheri a perpetual, royalty-free license to use, distribute, and sublicense your contribution as part of AIFLC.

---

## Commercial Services

### Q: If AIFLC is free, how does the author generate revenue?

**A:** Through value-added commercial services: implementation advisory, consulting engagements, training programs, certification, and planned enterprise extensions. For service enquiries, contact via [LinkedIn](https://www.linkedin.com/in/mohammad-maheri-8399565b) or mohammad.maheri.work@gmail.com.

---

### Q: Do I need to engage commercial services to use AIFLC?

**A:** No. The software is free and fully functional without any engagement. Commercial services are available for organisations that want expert guidance, faster adoption, or official training — not as a requirement.

---

## Enforcement

### Q: What happens if someone distributes AIFLC without the attribution notice?

**A:** It is a breach of the license. The author may contact the party to request compliance (30-day cure period), and if unresolved, may pursue remedies under applicable copyright law.

---

### Q: Does Apache 2.0 protect the author from liability if something goes wrong?

**A:** Yes. Apache 2.0 Section 7 provides a full disclaimer of warranties, and Section 8 limits liability for all contributors. AIFLC is provided "AS IS" without warranties of any kind. Users assume all risk associated with their use of the software. See `LICENSE` for the full disclaimer text.

---

## Brownfield Deployment (Existing Projects)

### Q: I injected AIFLC packages into an existing (brownfield) project and it damaged my work. Who is responsible?

**A:** You are. AIFLC is provided **"AS IS"** under Apache 2.0 Section 7 — without warranties of any kind, including fitness for a particular purpose. You are solely responsible for determining whether the packages are appropriate for your existing environment. The author and all contributors accept no liability for damages caused by deploying packages into existing workspaces.

---

### Q: What if AIFLC templates or scaffolding overwrite my existing files, configurations, or documentation?

**A:** Apache 2.0 Section 8 explicitly disclaims liability for all damages, including work stoppage, data loss, and all commercial losses. Before injecting any AIFLC package into an existing workspace, you should:

1. **Back up your project** (or ensure your work is committed to version control)
2. **Review what the package generates** — each package documents its output structure
3. **Use a test branch** — try injection in an isolated branch before applying to your main codebase

The author recommends these precautions but cannot enforce them. Failure to take precautions does not create any liability on the part of the author.

---

### Q: If AIFLC causes me to miss my obligations to my own clients (deadlines, deliverables, compliance requirements), can I hold the author responsible?

**A:** No. Apache 2.0 Section 8 disclaims liability for "all other commercial damages or losses" — this includes consequential damages such as missed deadlines, lost contracts, regulatory non-compliance, or any downstream obligation you owe to third parties. Your obligations to your clients are between you and them; they are not transferred to the AIFLC author by your choice to adopt the software.

---

### Q: Does damaging my own project release me from the Attribution Addendum?

**A:** No. The Attribution Addendum applies to any distributed product based on AIFLC regardless of whether the integration was successful, partial, or damaging. If you distribute a product or deliverable incorporating AIFLC content — even if it didn't work as you hoped — attribution remains required.

---

### Q: I lost source code or proprietary content because of an AIFLC package overwriting files. Do I have any claim?

**A:** No. The disclaimer is explicit: the work is provided without warranty and the user assumes all risks. Source control (git), backups, and proper evaluation before deployment are the user's responsibility. The author has no obligation to assist in recovery, provide support, or compensate for lost data — regardless of the cause.

---

### Q: Does purchasing commercial services change the liability position?

**A:** Commercial service engagements (advisory, consulting, training) are governed by their own services agreement, which will contain its own liability terms. However, the **open-source software itself** remains "AS IS" regardless of whether you are also a commercial services client. The software license and the services agreement are separate instruments.

---

## Contact Changes

### Q: What if the LinkedIn URL or email in the attribution notice becomes unreachable?

**A:** The attribution obligation remains regardless of whether specific URLs change over time. If the LinkedIn URL in the notice becomes unreachable, you are still required to include the attribution text as written. The current canonical contact details and source repository can always be found at:

- **Repository:** https://github.com/mbmd/AIFLC
- **Email:** mohammad.maheri.work@gmail.com

If you become aware that the attribution link has changed, updating it in your next release is good practice — but you are not in breach for linking to the URL that was current when you adopted the license.

---

*Document Status: DRAFT*  
*Last Updated: 2026-06-13*
