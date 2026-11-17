import { InboundForm } from "@/components/inbound-form";
import { pageMetadata } from "@/lib/site";

export const metadata = pageMetadata(
  "/contact/",
  "Request a demo",
  "Tell us who you are and what you would like to see.",
);

export default function ContactPage() {
  return (
    <article className="max-w-3xl space-y-8 py-16 sm:py-24">
      <div className="space-y-4">
        <h1 className="text-4xl font-semibold tracking-tight text-balance sm:text-5xl">
          Request a demo
        </h1>
        <p className="text-lg text-pretty text-muted-foreground">
          Tell us who you are and what you would like to see. We answer every
          request.
        </p>
      </div>
      <InboundForm />
    </article>
  );
}
