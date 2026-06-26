import { resolveSidecarBaseUrl } from './local-config';

export const checkSidecarHealth = async () => {
  try {
    const response = await fetch(`${resolveSidecarBaseUrl()}/health`);
    return response.ok;
  } catch {
    return false;
  }
};
