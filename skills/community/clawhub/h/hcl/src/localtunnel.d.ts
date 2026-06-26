declare module "localtunnel" {
  type Tunnel = {
    url: string;
  };

  type Localtunnel = (options: { port: number }) => Promise<Tunnel>;

  const localtunnel: Localtunnel;
  export default localtunnel;
}
